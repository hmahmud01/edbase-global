# Generated by Django 3.2.18 on 2023-05-30 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('global', '0029_rename_zipcontent_topicexercise_exercises'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topiccontent',
            name='detail',
        ),
        migrations.RemoveField(
            model_name='topiccontent',
            name='title',
        ),
    ]