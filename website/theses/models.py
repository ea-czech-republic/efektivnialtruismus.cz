import logging
from textwrap import dedent
from typing import Iterable

from django import forms
from django.db import models
from django.http import JsonResponse, HttpResponseRedirect
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.admin.edit_handlers import (
    StreamFieldPanel,
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.admin.utils import send_mail
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtailmenus.models import MenuPage

from theses import utils
from theses.forms import SimpleContactForm
from theses.outline_utils import _HeadingBlock, NestedOutline, FlatLinksOutline
from theses.views import conversion

logger = logging.getLogger(__name__)

THESES_MAILS = ["david.janku@effectivethesis.org"]
THESES_MAILS_2 = ["silvana.hultsch@effectivethesis.org"]

ALL_HEADINGS_RICH_TEXT_FEATURES = [
    "bold",
    "italic",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ol",
    "ul",
    "hr",
    "link",
    "document-link",
    "image",
    "embed",
]


class AllHeadingsRichTextBlock(blocks.RichTextBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, features=ALL_HEADINGS_RICH_TEXT_FEATURES, **kwargs)


class AllHeadingsRichTextField(RichTextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, features=ALL_HEADINGS_RICH_TEXT_FEATURES, **kwargs)


class HeadingBlock(blocks.RichTextBlock, _HeadingBlock):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value=value, parent_context=parent_context)
        context.update(self._get_additional_context(value.source))
        return context

    class Meta:
        template = "blocks/heading.html"


@register_snippet
class ThesisProvider(models.Model):
    provider_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    name = models.CharField(max_length=100, blank=False, unique=True)
    link = models.URLField(blank=False)
    description = RichTextField(blank=True)

    panels = [
        ImageChooserPanel("provider_image"),
        FieldPanel("name"),
        FieldPanel("link"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class ThesisDiscipline(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    introduction = RichTextField(blank=True)
    description_legacy = RichTextField(blank=True)
    topics = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            (
                "heading_linkable",
                HeadingBlock(
                    help_text="heading text",
                    features=["bold", "italic", "h1", "h2", "h3", "h4", "h5", "h6"],
                ),
            ),
            ("paragraph", AllHeadingsRichTextBlock()),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock()),
            ("rawHtml", blocks.RawHTMLBlock()),
        ],
        null=True,
        blank=True,
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("introduction"),
        StreamFieldPanel("topics"),
        FieldPanel("description_legacy"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class Coach(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    description = AllHeadingsRichTextField()

    panels = [
        FieldPanel("name"),
        FieldPanel("photo"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Coaches"


class ThesisPageTag(TaggedItemBase):
    content_object = ParentalKey("theses.ThesisPage", related_name="tagged_items")


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


def get_standard_streamfield():
    return StreamField(
        [
            ("rawHtml", blocks.RawHTMLBlock()),
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock()),
        ],
        null=True,
        blank=True,
    )


class ThesisSearch(Page, FlatLinksOutline):
    parent_page_types = ["theses.ThesisIndexPage"]

    body = get_standard_streamfield()
    body_secondary = get_standard_streamfield()
    footer = get_standard_streamfield()
    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
        StreamFieldPanel("body_secondary"),
        StreamFieldPanel("footer"),
    ]

    def _get_discipline_by_name(self, name) -> ThesisDiscipline:
        return ThesisDiscipline.objects.get(name=name)

    def get_context(self, request, *args, form=None, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if "discipline" in request.GET:
            discipline_name = request.GET["discipline"]
            discipline = self._get_discipline_by_name(name=discipline_name)
            context["selectedDiscipline"] = discipline_name
            context["descriptionLegacy"] = discipline.description_legacy
            context["introduction"] = discipline.introduction
            context["disciplineTopics"] = discipline.topics
            context["topicsOutline"] = self.get_outline(discipline.topics.stream_data)

        context["disciplines"] = ThesisDiscipline.objects.all().order_by("name")

        return context

    def serve(self, request, *args, **kwargs):
        if "discipline" in request.GET:
            discipline_name = request.GET["discipline"]
            if discipline_name in ("biology", "medicine"):
                return HttpResponseRedirect(
                    request.path_info + "?discipline=life+sciences#disciplines"
                )
            if discipline_name in ("physics", "mathematics statistics"):
                return HttpResponseRedirect(
                    request.path_info
                    + "?discipline=mathematics+statistics+physics#disciplines"
                )
        return super().serve(request)


class ThesisIndexPage(Page):
    text_phd = get_standard_streamfield()
    text_nonphd = get_standard_streamfield()
    column_1 = get_standard_streamfield()
    column_2 = get_standard_streamfield()
    column_3 = get_standard_streamfield()
    references_1 = get_standard_streamfield()
    references_2 = get_standard_streamfield()
    body = get_standard_streamfield()

    content_panels = Page.content_panels + [
        StreamFieldPanel("text_phd"),
        StreamFieldPanel("text_nonphd"),
        StreamFieldPanel("column_1"),
        StreamFieldPanel("column_2"),
        StreamFieldPanel("column_3"),
        StreamFieldPanel("references_1"),
        StreamFieldPanel("references_2"),
        StreamFieldPanel("body"),
    ]

    def get_context(self, request):
        context = super(ThesisIndexPage, self).get_context(request)
        context["text_phd"] = self.text_phd
        context["text_nonphd"] = self.text_nonphd

        coaches = Coach.objects.all().order_by("name")
        groups = list(utils.chunks(coaches, 3))
        if groups:
            context["coach_groups"] = groups
        return context


class ThesisCoachingPage(Page):
    parent_page_types = ["theses.ThesisIndexPage"]

    body = get_standard_streamfield()
    body2 = get_standard_streamfield()
    footer = get_standard_streamfield()

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
        StreamFieldPanel("body2"),
        StreamFieldPanel("footer"),
    ]


class ThesisChooseHelpPage(Page):
    parent_page_types = ["theses.ThesisIndexPage"]

    impact = get_standard_streamfield()
    career = get_standard_streamfield()
    research = get_standard_streamfield()

    body = get_standard_streamfield()

    content_panels = Page.content_panels + [
        StreamFieldPanel("impact"),
        StreamFieldPanel("career"),
        StreamFieldPanel("research"),
        StreamFieldPanel("body"),
    ]


class ThesisPage(Page):
    description = RichTextField()
    why_important = RichTextField()
    sources = RichTextField()
    tags = ClusterTaggableManager(through=ThesisPageTag, blank=True)
    provider = models.ForeignKey(
        "theses.ThesisProvider", default=1, on_delete=models.SET_NULL, null=True
    )
    discipline = ParentalManyToManyField("theses.ThesisDiscipline", blank=False)

    search_fields = Page.search_fields + [
        index.SearchField("description"),
        index.SearchField("why_important"),
        index.SearchField("sources"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("why_important"),
        FieldPanel("tags"),
        FieldPanel("sources"),
        FieldPanel("discipline", widget=forms.CheckboxSelectMultiple),
        SnippetChooserPanel("provider"),
    ]

    promote_panels = [MultiFieldPanel(Page.promote_panels, "Common page configuration")]

    parent_page_types = ["theses.ThesisIndexPage"]

    def serve(self, request):
        if request.method == "POST":
            from theses.forms import InterestsForm

            form = InterestsForm(request.POST)
            if form.is_valid():
                form.clean()
                absolute_uri = request.build_absolute_uri()
                mail_content = self.build_mail_content(absolute_uri, form.cleaned_data)
                thesis_title = form.cleaned_data["thesis_title"]

                send_mail(
                    "Thesis interest: {}".format(thesis_title),
                    mail_content,
                    THESES_MAILS,  # recipient email
                    form.cleaned_data["contact_email"],
                )

                return conversion(request, absolute_uri, thesis_title)
            else:
                logger.error("The submitted form was invalid.")
                return super(ThesisPage, self).serve(request)
        else:
            return super(ThesisPage, self).serve(request)

    def get_context(self, request):
        from theses.forms import InterestsForm

        context = super(ThesisPage, self).get_context(request)
        context["contactForm"] = InterestsForm
        context["thesis_title"] = self.title
        return context

    @staticmethod
    def build_mail_content(uri, data):
        return dedent(
            """
        Thesis: {thesis_uri}
        Name: {contact_name},
        Contact email: {contact_email},
        Course and University: {course_and_university},
        Deadline: {deadline}
        How did you found about the website: {find_out_website},
        
        --------Message--------
        {content}
        """.format(
                thesis_uri=uri, **data
            )
        )


class ThesisSimple(Page):
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock()),
            ("rawHtml", blocks.RawHTMLBlock()),
            (
                "medailon",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(required=True)),
                        ("pic", ImageChooserBlock(required=True)),
                        ("description", blocks.RichTextBlock(required=True)),
                    ],
                    template="blocks/medailon.html",
                    icon="user",
                ),
            ),
        ]
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]

    parent_page_types = ["theses.ThesisIndexPage"]

    @staticmethod
    def build_mail_content_contact(data):
        return dedent(
            """
        Name: {contact_name},
        Contact email: {contact_email},

        --------Message--------
        {content}
        """.format(
                **data
            )
        )

    def serve(self, request):
        if request.method == "POST":
            form_slug = request.POST.get("formSlug")
            if "simpleContactForm" == form_slug:
                form = SimpleContactForm(request.POST)
                if form.is_valid():
                    form.clean()
                    send_mail(
                        "Contacting using Contact Form",
                        self.build_mail_content_contact(form.cleaned_data),
                        THESES_MAILS,  # recipient email
                        form.cleaned_data["contact_email"],
                    )

                    return JsonResponse(
                        {
                            "message": "Thank you for your interest! "
                            "We will let get back to you soon!"
                        }
                    )
        else:
            return super(ThesisSimple, self).serve(request)

    def get_context(self, request):
        context = super(ThesisSimple, self).get_context(request)
        context["contactForm"] = SimpleContactForm
        return context


class OutlineThesisSimple(Page, NestedOutline):
    outline_title = RichTextField()
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            (
                "heading_linkable",
                HeadingBlock(
                    help_text="heading text",
                    features=["h1", "h2", "h3", "h4", "h5", "h6"],
                ),
            ),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock()),
            ("rawHtml", blocks.RawHTMLBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("outline_title"),
        StreamFieldPanel("body"),
    ]

    parent_page_types = ["theses.ThesisIndexPage"]

    def get_context(self, request):
        context = super(OutlineThesisSimple, self).get_context(request)
        context["contactForm"] = SimpleContactForm
        context["outline"] = self.get_outline(self.body.stream_data)
        return context


class ThesisFinishedIndexPage(Page):
    body = get_standard_streamfield()
    footer = get_standard_streamfield()

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
        StreamFieldPanel("footer"),
    ]

    def get_context(self, request, **kwargs):
        context = super(ThesisFinishedIndexPage, self).get_context(request, **kwargs)
        theses = list(self.get_children().live())
        groups = list(utils.chunks(theses, 3))
        context["preview_group"] = groups[0]
        context["collapsed_groups"] = groups[1:]
        return context


class ThesisFinishedPage(Page):
    body = get_standard_streamfield()
    about_author = RichTextField()

    pdf_thesis = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    pdf_thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    author_pic = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        DocumentChooserPanel("pdf_thesis"),
        ImageChooserPanel("pdf_thumbnail"),
        ImageChooserPanel("author_pic"),
        FieldPanel("about_author"),
        StreamFieldPanel("body"),
    ]

    parent_page_types = ["theses.ThesisFinishedIndexPage"]

    def prev(self):
        prev_sibling = self.get_prev_sibling()
        if prev_sibling:
            if prev_sibling.live:
                return prev_sibling
            else:
                return prev_sibling.prev()

    def next(self):
        next_sibling = self.get_next_sibling()
        if next_sibling:
            if next_sibling.live:
                return next_sibling
            else:
                return next_sibling.next()


class OtherServicesPage(Page):
    body = get_standard_streamfield()

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]


class SubmenuItem(Orderable):
    page = models.ForeignKey("wagtailcore.Page", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    url_suffix = models.CharField("Append to URL", blank=True, max_length=255)
    submenu_page = ParentalKey(
        "theses.SubmenuPage", on_delete=models.CASCADE, related_name="submenu_items"
    )

    panels = [
        PageChooserPanel("page"),
        FieldPanel("title"),
        FieldPanel("url_suffix"),
    ]

    def get_submenu_data(self, current_site):
        page: Page = self.page
        url = page.relative_url(current_site)
        if self.url_suffix:
            url += self.url_suffix
        title = self.title if self.title else page.title
        return {"text": title, "href": url}


class SubmenuPage(MenuPage):
    content_panels = Page.content_panels + [
        InlinePanel("submenu_items", label="Submenu Items"),
    ]

    def modify_submenu_items(self, menu_items, **kwargs):
        menu_items = super(SubmenuPage, self).modify_submenu_items(menu_items, **kwargs)
        submenu_items: Iterable[SubmenuItem] = self.submenu_items.all()

        menu_items.extend(
            (item.get_submenu_data(kwargs["current_site"]) for item in submenu_items)
        )
        return menu_items

    def has_submenu_items(self, **kwargs):
        return self.submenu_items.exists()
