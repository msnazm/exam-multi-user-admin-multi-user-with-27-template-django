# Generated by Django 3.2.9 on 2022-01-15 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_imageexam'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imageexam',
            old_name='imageone',
            new_name='image',
        ),
    ]
