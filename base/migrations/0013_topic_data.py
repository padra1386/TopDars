# Generated by Django 4.1.6 on 2023-02-21 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_topic_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='data',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
