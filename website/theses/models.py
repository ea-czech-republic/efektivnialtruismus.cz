from django.db import models
from django.contrib.contenttypes.models import ContentType

from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField

from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from taggit.models import Tag

class ThesisPageTag(TaggedItemBase):
    content_object = ParentalKey('theses.ThesisPage', related_name='tagged_items')

class ThesisIndexPage(Page):
    intro = StreamField([
        ('rawHtml', blocks.RawHTMLBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('intro'),

    ]

    def get_context(self, request):
        context = super(ThesisIndexPage, self).get_context(request)
        context['theses'] = ThesisPage.objects.child_of(self).live().order_by('-first_published_at')
        context["tags"] = ThesisPage.tags.all()
        return context


    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in ThesisIndexPage._meta.fields]

    def cur_site_id(self):
        return "{}".format(self.get_url_parts()[0])




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



    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in ThesisPage._meta.fields]

    def cur_site_id(self):
        return "{}".format(self.get_url_parts()[0])

