from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
import datetime


class MedailonBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)

    def get_context(self, value, parent_context=None):
        context = super(MedailonBlock, self).get_context(value, parent_context=parent_context)
        context['is_happening_today'] = (value['date'] == datetime.date.today())
        return context


class HomePage(Page):
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
