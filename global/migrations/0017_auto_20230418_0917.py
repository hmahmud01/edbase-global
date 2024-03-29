# Generated by Django 3.2.16 on 2023-04-18 09:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('global', '0016_course_thumb'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubsciptionKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriptionKey', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('amount', models.FloatField()),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='fee',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
