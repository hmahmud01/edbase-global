# Generated by Django 3.2.15 on 2022-11-01 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global', '0008_studentcountryindex'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.TextField(blank=True, null=True)),
                ('seen', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]
