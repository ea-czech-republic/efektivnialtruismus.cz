# Generated by Django 2.2.1 on 2020-05-23 16:37

from django.db import migrations, models
import django.db.models.deletion
import theses.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('theses', '0036_thesiscoachingpage_body2'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutlineThesisSimple',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('outline_title', wagtail.core.fields.RichTextField()),
                ('body', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('heading_linkable', theses.models.HeadingBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], help_text='heading text')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('rawHtml', wagtail.core.blocks.RawHTMLBlock())])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]