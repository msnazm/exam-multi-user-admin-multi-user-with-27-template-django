# Generated by Django 3.2.9 on 2022-01-11 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_remove_choice_repeat_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
