# Generated by Django 3.2.16 on 2023-04-18 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global', '0017_auto_20230418_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='subsciptionkey',
            name='shortKey',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
