import logging
from textwrap import dedent

from django.db import models
from django.http import JsonResponse
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.wagtailadmin.utils import send_mail
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from django import forms
from wagtail.wagtailsnippets.models import register_snippet

from theses.forms import ProposalForm, SimpleContactForm, DisciplineSelect
from theses.views import conversion

logger = logging.getLogger(__name__)

THESES_MAILS = ['theses@efektivni-altruismus.cz']


@register_snippet
class ThesisProvider(models.Model):
    provider_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    name = models.CharField(max_length=100, blank=False, unique=True)
    link = models.URLField(blank=False)
    description = RichTextField(blank=True)

    panels = [
        ImageChooserPanel('provider_image'),
        FieldPanel('name'),
        FieldPanel('link'),
        FieldPanel('description')
    ]

    def __str__(self):
        return self.name


@register_snippet
class ThesisDiscipline(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = RichTextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('description')
    ]

    def __str__(self):
        return self.name


class ThesisPageTag(TaggedItemBase):
    content_object = ParentalKey('theses.ThesisPage',
                                 related_name='tagged_items')


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


def get_standard_streamfield():
    return StreamField([
        ('rawHtml', blocks.RawHTMLBlock()),
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),

    ], null=True, blank=True)


class ThesisSearch(Page):
    parent_page_types = ['theses.ThesisIndexPage']

    body = get_standard_streamfield()

    def get_context(self, request):
        context = super(ThesisSearch, self).get_context(request)
        if 'discipline' in request.GET:
            discipline_name = request.GET['discipline']
            discipline = ThesisDiscipline.objects.get(name=discipline_name)
            theses = ThesisPage.objects.filter(discipline=discipline).live().order_by('?')
            # filter only those from the list above
            tags_qs = theses.values('tags').distinct()
            tags = ThesisPage.tags.filter(pk__in=[x['tags'] for x in tags_qs])
            discipline_form = DisciplineSelect({'discipline': discipline_name})
        else:
            theses = None
            tags = None
            discipline_form = DisciplineSelect

        context['theses'] = theses
        context['tags'] = tags
        context['disciplineSelectForm'] = discipline_form

        return context


class ThesisIndexPage(Page):
    column_1 = get_standard_streamfield()
    column_2 = get_standard_streamfield()
    column_3 = get_standard_streamfield()
    references_1 = get_standard_streamfield()
    references_2 = get_standard_streamfield()
    body = get_standard_streamfield()

    content_panels = Page.content_panels + [
        StreamFieldPanel('column_1'),
        StreamFieldPanel('column_2'),
        StreamFieldPanel('column_3'),
        StreamFieldPanel('references_1'),
        StreamFieldPanel('references_2'),
        StreamFieldPanel('body'),
    ]


class ThesisChooseHelpPage(Page):
    parent_page_types = ['theses.ThesisIndexPage']

    impact = get_standard_streamfield()
    career = get_standard_streamfield()
    research = get_standard_streamfield()

    body = get_standard_streamfield()

    content_panels = Page.content_panels + [
        StreamFieldPanel('impact'),
        StreamFieldPanel('career'),
        StreamFieldPanel('research'),
        StreamFieldPanel('body'),
    ]


class ThesisPage(Page):
    description = RichTextField()
    why_important = RichTextField()
    sources = RichTextField()
    tags = ClusterTaggableManager(through=ThesisPageTag, blank=True)
    provider = models.ForeignKey('theses.ThesisProvider', default=1, on_delete=models.SET_NULL, null=True)
    discipline = ParentalManyToManyField('theses.ThesisDiscipline', blank=False)

    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.SearchField('why_important'),
        index.SearchField('sources'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('why_important'),
        FieldPanel('tags'),
        FieldPanel('sources'),
        FieldPanel('discipline', widget=forms.CheckboxSelectMultiple),
        SnippetChooserPanel('provider'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    parent_page_types = ['theses.ThesisIndexPage']

    def serve(self, request):
        if request.method == 'POST':
            from theses.forms import InterestsForm
            form = InterestsForm(request.POST)
            if form.is_valid():
                form.clean()
                absolute_uri = request.build_absolute_uri()
                mail_content = self.build_mail_content(absolute_uri, form.cleaned_data)
                thesis_title = form.cleaned_data['thesis_title']

                send_mail('Thesis interest: {}'.format(thesis_title),
                          mail_content,
                          THESES_MAILS,  # recipient email
                          form.cleaned_data['contact_email']
                          )

                return conversion(request, absolute_uri, thesis_title)
            else:
                logger.error('The submitted form was invalid.')
                return super(ThesisPage, self).serve(request)
        else:
            return super(ThesisPage, self).serve(request)

    def get_context(self, request):
        from theses.forms import InterestsForm
        context = super(ThesisPage, self).get_context(request)
        context["contactForm"] = InterestsForm
        context['thesis_title'] = self.title
        return context

    @staticmethod
    def build_mail_content(uri, data):
        return dedent("""
        Thesis: {thesis_uri}
        Name: {contact_name},
        Contact email: {contact_email},
        Course and University: {course_and_university},
        Deadline: {deadline}
        
        --------Message--------
        {content}
        """.format(thesis_uri=uri, **data))


class ThesisSimple(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
        ('rawHtml', blocks.RawHTMLBlock()),
        ('medailon', blocks.StructBlock(
            [
                ('title', blocks.CharBlock(required=True)),
                ('pic', ImageChooserBlock(required=True)),
                ('description', blocks.RichTextBlock(required=True)),
            ],
            template='blocks/medailon.html',
            icon='user'
        ))
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['theses.ThesisIndexPage']

    @staticmethod
    def build_mail_content_contact(data):
        return dedent("""
        Name: {contact_name},
        Contact email: {contact_email},

        --------Message--------
        {content}
        """.format(**data))

    @staticmethod
    def build_mail_content_propose(data):
        return dedent("""
        Name: {contact_name},
        Contact email: {contact_email},
        Organisation: {organisation},
        
        Title: {title},
        Description: {description},
        Why is it important: {why_important},
        Sources: {sources},
        --------Message--------
        {message}
        """.format(**data))

    def serve(self, request):
        if request.method == 'POST':
            form_slug = request.POST.get('formSlug')
            if 'simpleContactForm' == form_slug:
                form = SimpleContactForm(request.POST)
                if form.is_valid():
                    form.clean()
                    send_mail('Contacting using Contact Form',
                              self.build_mail_content_contact(form.cleaned_data),
                              THESES_MAILS,  # recipient email
                              form.cleaned_data['contact_email']
                              )

                    return JsonResponse({'message': 'Thank you for your interest! '
                                                    'We will let get back to you soon!'})
            elif 'proposalForm' == form_slug:
                form = ProposalForm(request.POST)
                if form.is_valid():
                    form.clean()
                    send_mail('Contacting using Contact Form',
                              self.build_mail_content_propose(form.cleaned_data),
                              THESES_MAILS,  # recipient email
                              form.cleaned_data['contact_email']
                              )

                    return JsonResponse({'message': 'Thank you for the proposal! '
                                                    'We will let get back to you soon!'})
        else:
            return super(ThesisSimple, self).serve(request)

    def get_context(self, request):
        context = super(ThesisSimple, self).get_context(request)
        context["contactForm"] = SimpleContactForm
        context["proposalForm"] = ProposalForm
        return context
