# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-06 18:20
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0010_thesisindexpage_propose'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesisindexpage',
            name='header',
            field=wagtail.core.fields.StreamField((('rawHtml', wagtail.core.blocks.RawHTMLBlock()), ('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock())), default=None),
            preserve_default=False,
        ),
    ]
