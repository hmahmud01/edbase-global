# Generated by Django 3.2.18 on 2023-09-10 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global', '0036_interactivemodule'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
