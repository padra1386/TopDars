# Generated by Django 4.1.6 on 2023-06-04 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0002_video_like_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_url',
            field=models.TextField(),
        ),
    ]
