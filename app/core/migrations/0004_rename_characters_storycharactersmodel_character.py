# Generated by Django 5.1.6 on 2025-03-06 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_linksmodel_colour'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storycharactersmodel',
            old_name='characters',
            new_name='character',
        ),
    ]
