from __future__ import annotations
import logging
import re
from textwrap import dedent
from typing import List, Tuple

from django.contrib import messages
from django.db import models
from django.http import JsonResponse, HttpResponseRedirect
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.admin.utils import send_mail
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.core.rich_text import RichText
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from django import forms
from wagtail.snippets.models import register_snippet

from theses import utils
from theses.forms import SimpleContactForm, TopicInterestForm
from theses.views import conversion, coaching_conversion

logger = logging.getLogger(__name__)

THESES_MAILS = ["david@effectivethesis.com"]


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
    description = RichTextField(blank=True)

    panels = [FieldPanel("name"), FieldPanel("description")]

    def __str__(self):
        return self.name


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


class ThesisSearch(Page):
    parent_page_types = ["theses.ThesisIndexPage"]

    body = get_standard_streamfield()
    body_secondary = get_standard_streamfield()
    footer = get_standard_streamfield()
    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
        StreamFieldPanel("body_secondary"),
        StreamFieldPanel("footer"),
    ]

    def get_context(self, request, *args, form=None, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if "discipline" in request.GET:
            discipline_name = request.GET["discipline"]
            discipline = ThesisDiscipline.objects.get(name=discipline_name)
            selected_discipline = discipline_name
            selected_discipline_description = discipline.description
        else:
            selected_discipline = None
            selected_discipline_description = None

        context["selectedDiscipline"] = selected_discipline
        context["selectedDisciplineDescription"] = selected_discipline_description
        context["disciplines"] = ThesisDiscipline.objects.all().order_by("name")
        context["form"] = form or TopicInterestForm()

        return context

    @staticmethod
    def build_mail_content(uri, data):
        return dedent(
            """
        Name: {contact_name},
        Contact email: {contact_email},
        How did they find out about this website: {where_from},
        
        --------Message--------
        {content}
        """.format(
                **data
            )
        )

    def serve(self, request, *args, **kwargs):
        if request.method == "POST":
            form = TopicInterestForm(request.POST)
            if form.is_valid():
                mail_content = self.build_mail_content(
                    request.build_absolute_uri(), form.cleaned_data
                )
                send_mail(
                    subject="Topic interest",
                    message=mail_content,
                    recipient_list=THESES_MAILS,
                    from_email=form.cleaned_data["contact_email"],
                )
                messages.success(request, "Thank you for your interest!")
                return HttpResponseRedirect(request.path_info + "#topic-interest-form")
            else:
                return super().serve(request, form=form)
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

    def get_context(self, request, errored_form=None):
        from theses.forms import CoachingForm

        context = super().get_context(request)
        context["contactForm"] = errored_form or CoachingForm

        return context

    @staticmethod
    def build_mail_content(data):
        return dedent(
            """
        Name: {contact_name},
        Contact email: {contact_email},
        Course and University: {university},
        Seniority: {seniority},
        Career: {career},
        Requirements: {requirements},
        Preferences: {preferences},
        Knowledgeable: {read_above},
        Deadline for selection: {deadline},
        CV: {cv_url},
        Deadline for submission: {deadline_submit},
        Anything else: {anything_else},
        How did you found about the website: {find_out_website},
        """.format(
                **data
            )
        )

    def serve(self, request):
        if request.method == "POST":
            print("posting")
            from theses.forms import CoachingForm

            form = CoachingForm(request.POST)
            if form.is_valid():
                print("form is valid")
                form.clean()
                mail_content = self.build_mail_content(form.cleaned_data)
                contact_name = form.cleaned_data["contact_name"]

                send_mail(
                    "Thesis coaching interest: {}".format(contact_name),
                    mail_content,
                    THESES_MAILS,  # recipient email
                    form.cleaned_data["contact_email"],
                )

                return coaching_conversion(request)
            else:
                print("form is invalid")
                logger.error("The submitted form was invalid.")
                return super().serve(request, errored_form=form)
        else:
            return super().serve(request)


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


class HeadingBlock(blocks.RichTextBlock):
    @staticmethod
    def _get_title(m):
        title = m.group("title")
        to_drop = ("<br/>", r"<h\d>", r"</h\d>")
        for text in to_drop:
            title = re.sub(text, "", title)
        return title.strip()

    @staticmethod
    def _get_link(title):
        return title.lower().replace(" ", "-")

    @classmethod
    def _get_additional_context(cls, _value):

        if isinstance(_value, RichText):  # in case of using Preview
            _value = _value.source
        m = re.search("<h(?P<heading_size>\d)>(?P<title>.*)</h\d>", _value)
        if not m:
            return {}

        title = cls._get_title(m)
        return dict(
            title=title,
            link=cls._get_link(title),
            heading_size=m.group("heading_size"),
        )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value=value, parent_context=parent_context)
        context.update(self._get_additional_context(value.source))
        return context

    class Meta:
        template = "blocks/heading.html"


class Heading:
    title: str
    link: str
    size: int
    nested_headings: List[Heading]

    def __init__(self, title, link, heading_size):
        self.title = title
        self.link = link
        self.size = int(heading_size)
        self.nested_headings = []

    def to_html(self):
        nested_html = headings_to_html(self.nested_headings)
        _html = f"<li><a href='#{self.link}'>{self.title}</a>{nested_html}</li>"
        return _html


def headings_to_html(headings: List[Heading]):
    _nested_htmls = "".join(_heading.to_html() for _heading in headings)
    nested_html = f"<ul>{_nested_htmls}</ul>" if _nested_htmls else ""
    return nested_html


class OutlineThesisSimple(Page):
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

    def serve(self, request):
        if request.method == "GET":
            res = super(OutlineThesisSimple, self).serve(request)
            return res

    @staticmethod
    def _get_heading(_data):
        if isinstance(_data, tuple):
            keys = ("type", "value", "id")
            _data = dict(zip(keys, _data))

        if _data["type"] == "heading_linkable":
            source = _data["value"]
            return HeadingBlock._get_additional_context(source)
        return None

    def _get_headings(self, stream_data):
        headings = (self._get_heading(data) for data in stream_data)
        return [Heading(**heading) for heading in headings if heading]

    def _place_heading_into_structure(
        self, heading: Heading, structure: List[Heading]
    ) -> List[Heading]:
        if not structure:
            return [heading]

        if heading.size <= structure[-1].size:
            structure.append(heading)
            return structure

        _structure = self._place_heading_into_structure(
            heading, structure[-1].nested_headings
        )
        structure[-1].nested_headings = _structure
        return structure

    def _nest_headings(self, headings: list):
        if not headings:
            return []

        structure = []
        for heading in headings:
            structure = self._place_heading_into_structure(heading, structure)

        return structure

    def _get_outline(self, stream_data) -> str:
        headings = self._get_headings(stream_data)
        headings_nested = self._nest_headings(headings)
        return headings_to_html(headings_nested)

    def get_context(self, request):
        context = super(OutlineThesisSimple, self).get_context(request)
        context["contactForm"] = SimpleContactForm
        context["outline"] = self._get_outline(self.body.stream_data)
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
        blank=False,
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
