# Generated by Django 5.1.6 on 2025-03-03 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vaksmodel',
            old_name='height',
            new_name='sound',
        ),
    ]
