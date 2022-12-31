# Generated by Django 3.2.9 on 2022-01-13 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_rename_correct_questuion_answer_correct_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceArchive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datecreate', models.CharField(max_length=50)),
                ('datecreatealt', models.BigIntegerField()),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('timespent_s', models.IntegerField()),
                ('timespent_m', models.IntegerField()),
                ('timespent_h', models.IntegerField()),
                ('repeat_quiz', models.IntegerField()),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.answer')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.question')),
                ('quiz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.quiz')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]