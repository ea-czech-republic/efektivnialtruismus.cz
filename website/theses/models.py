from django.db import models
from django.http import HttpResponse, JsonResponse
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

    content_panels = Page.content_panels + [
        StreamFieldPanel('intro'),

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
    name = models.CharField(max_length=30, blank=False)
    description = RichTextField(blank=True)

    panels = [
        ImageChooserPanel('provider_image'),
        FieldPanel('name'),
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
            print('asdasd', request.get_full_path())
            from theses.forms import ContactForm
            form = ContactForm(request.POST)
            if form.is_valid():
                form.clean()
                data = form.cleaned_data
                print(data['content'])
                send_mail('Thesis proposal',
                          data['content'],
                          ['kotrfa@gmail.com'],  # recipient email
                          data['contact_email']
                          )
                return JsonResponse({'contentMessage': 'sent major!'})
        else:
            return super(ThesisPage, self).serve(request)

    def get_context(self, request):
        from theses.forms import ContactForm
        context = super(ThesisPage, self).get_context(request)
        context["contactForm"] = ContactForm
        return context


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
