# Generated by Django 3.2.18 on 2023-04-18 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global', '0018_subsciptionkey_shortkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='zipContent',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='videoUrl',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
