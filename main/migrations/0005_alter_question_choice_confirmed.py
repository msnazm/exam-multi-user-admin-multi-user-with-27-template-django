# Generated by Django 3.2.9 on 2022-01-02 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_question_choice_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='choice_confirmed',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
