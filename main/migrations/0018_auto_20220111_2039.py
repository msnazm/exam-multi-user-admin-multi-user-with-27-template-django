# Generated by Django 3.2.9 on 2022-01-11 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_question_answer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answer_id',
        ),
        migrations.AddField(
            model_name='answer',
            name='correct_questuion',
            field=models.BooleanField(blank=True, default=0, null=True),
        ),
    ]