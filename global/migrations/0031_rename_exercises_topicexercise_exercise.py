# Generated by Django 3.2.18 on 2023-05-30 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('global', '0030_auto_20230530_1935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topicexercise',
            old_name='exercises',
            new_name='exercise',
        ),
    ]