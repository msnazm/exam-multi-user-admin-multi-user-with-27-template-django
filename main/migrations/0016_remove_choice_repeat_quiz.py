# Generated by Django 3.2.9 on 2022-01-10 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_choice_repeat_quiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='repeat_quiz',
        ),
    ]