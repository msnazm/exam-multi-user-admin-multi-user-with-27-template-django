# Generated by Django 3.2.9 on 2022-01-07 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_choice_timespent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='timespent',
            field=models.TimeField(),
        ),
    ]