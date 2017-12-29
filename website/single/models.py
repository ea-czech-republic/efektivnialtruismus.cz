from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from datetime import date


class MedailonBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)

    def get_context(self, value, parent_context=None):
        context = super(MedailonBlock, self).get_context(value, parent_context=parent_context)
        context['is_happening_today'] = (value['date'] == date.today())
        return context


class CfarPage(Page):
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


class PomahejPage(Page):
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


class RetreatPage(Page):
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
