# Generated by Django 2.2.1 on 2021-09-15 21:05

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0041_group_collection_permissions_verbose_name_plural"),
        ("theses", "0040_auto_20200831_0854"),
    ]

    operations = [
        migrations.CreateModel(
            name="OtherServicesPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                (
                    "body",
                    wagtail.core.fields.StreamField(
                        [
                            ("rawHtml", wagtail.core.blocks.RawHTMLBlock()),
                            (
                                "heading",
                                wagtail.core.blocks.CharBlock(classname="full title"),
                            ),
                            ("paragraph", wagtail.core.blocks.RichTextBlock()),
                            ("image", wagtail.images.blocks.ImageChooserBlock()),
                            ("embed", wagtail.embeds.blocks.EmbedBlock()),
                        ],
                        blank=True,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
