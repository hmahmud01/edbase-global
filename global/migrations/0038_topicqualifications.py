# Generated by Django 3.2.18 on 2023-09-11 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('global', '0037_topic_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicQualifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualifcation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='global.qualification')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='global.topic')),
            ],
        ),
    ]
