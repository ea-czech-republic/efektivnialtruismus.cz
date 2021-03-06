# Generated by Django 2.2.1 on 2019-10-06 13:20

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0033_thesiscoachingpage_footer'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesissearch',
            name='body_secondary',
            field=wagtail.core.fields.StreamField([('rawHtml', wagtail.core.blocks.RawHTMLBlock()), ('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock())], blank=True, null=True),
        ),
    ]
