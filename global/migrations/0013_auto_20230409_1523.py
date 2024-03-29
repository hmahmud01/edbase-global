# Generated by Django 3.2.18 on 2023-04-09 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('global', '0012_article_articlecategory_course_lecture_lecturemedia'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptioncode',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscriptioncode',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='global.usersubscription'),
        ),
        migrations.AlterField(
            model_name='subscriptioncode',
            name='ref',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='global.subscription'),
        ),
    ]
