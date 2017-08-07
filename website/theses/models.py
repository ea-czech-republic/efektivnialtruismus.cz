from django.db import models
from django.http import JsonResponse
from theses.forms import ProposalForm, InterestsForm, SimpleContactForm
from textwrap import dedent
from wagtail.wagtailcore import blocks
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from modelcluster.fields import ParentalKey
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin.utils import send_mail

THESES_MAILS = ['kotrfa@gmail.com']


class ThesisPageTag(TaggedItemBase):
    content_object = ParentalKey('theses.ThesisPage', related_name='tagged_items')


class ThesisIndexPage(Page):
    intro = StreamField([
        ('rawHtml', blocks.RawHTMLBlock()),
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),

    ])
    our_topics = StreamField([
        ('rawHtml', blocks.RawHTMLBlock()),
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),

    ])
    process = StreamField([
        ('rawHtml', blocks.RawHTMLBlock()),
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),

    ])

    propose = StreamField([
        ('rawHtml', blocks.RawHTMLBlock()),
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),

    ])
    header = StreamField([
        ('rawHtml', blocks.RawHTMLBlock()),
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('intro'),
        StreamFieldPanel('our_topics'),
        StreamFieldPanel('process'),
        StreamFieldPanel('propose'),
    ]

    def get_context(self, request):
        context = super(ThesisIndexPage, self).get_context(request)
        context['theses'] = ThesisPage.objects.child_of(self).live().order_by('-first_published_at')
        context["tags"] = ThesisPage.tags.all()
        return context


@register_snippet
class ThesisProvider(models.Model):
    provider_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    name = models.CharField(max_length=100, blank=False)
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


class ThesisPage(Page):
    description = RichTextField()
    why_important = RichTextField()
    sources = RichTextField()
    tags = ClusterTaggableManager(through=ThesisPageTag, blank=True)
    provider = models.ForeignKey(ThesisProvider, default=1, on_delete=models.SET_NULL, null=True)

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
                mail_content = self.build_mail_content(request.build_absolute_uri(), form.cleaned_data)
                send_mail('Thesis interest: {}'.format(request.POST['thesis_title']),
                          mail_content,
                          THESES_MAILS,  # recipient email
                          form.cleaned_data['contact_email']
                          )

                return JsonResponse({'message': 'Thank you for your interest! '
                                                'We will let get back to you soon!'})
        else:
            return super(ThesisPage, self).serve(request)

    def get_context(self, request):
        from theses.forms import InterestsForm
        context = super(ThesisPage, self).get_context(request)
        context["contactForm"] = InterestsForm
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
        ('rawHtml', blocks.RawHTMLBlock())
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
