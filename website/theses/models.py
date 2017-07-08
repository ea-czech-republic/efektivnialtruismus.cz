from wagtail.wagtailcore import blocks
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


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


class ThesisPage(Page):
    description = RichTextField()
    why_important = RichTextField()
    sources = RichTextField()
    tags = ClusterTaggableManager(through=ThesisPageTag, blank=True)

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
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    parent_page_types = ['theses.ThesisIndexPage']
