# Generated by Django 2.2.1 on 2020-08-31 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0038_coach'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thesisdiscipline',
            old_name='description',
            new_name='description_legacy',
        ),
    ]
