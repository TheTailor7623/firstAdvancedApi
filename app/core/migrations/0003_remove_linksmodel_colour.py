# Generated by Django 5.1.6 on 2025-03-05 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_height_vaksmodel_sound'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linksmodel',
            name='colour',
        ),
    ]
