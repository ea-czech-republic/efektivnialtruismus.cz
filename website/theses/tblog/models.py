from django.db import models

from wagtail.search import index
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core import blocks
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel


class ThesesBlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(ThesesBlogIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by("-blogpage__date")
        context["blogpages"] = blogpages
        return context

    def cur_site_id(self):
        return "{}".format(self.get_url_parts()[0])


class ThesesArticlePage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    author = models.CharField(max_length=50, blank=False)
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock()),
            ("rawHtml", blocks.RawHTMLBlock()),
        ]
    )

    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
        index.SearchField("author"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("author"),
        FieldPanel("intro"),
        StreamFieldPanel("body"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel("feed_image"),
    ]

    def cur_site_id(self):
        return "{}".format(self.get_url_parts()[0])
