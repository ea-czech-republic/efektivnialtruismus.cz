# Generated by Django 2.0.3 on 2018-08-13 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesesarticlepage',
            name='author',
            field=models.CharField(default='Fill Me!', max_length=50),
            preserve_default=False,
        ),
    ]
