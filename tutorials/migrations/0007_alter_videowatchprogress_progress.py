# Generated by Django 4.1.6 on 2023-06-04 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0006_alter_videowatchprogress_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videowatchprogress',
            name='progress',
            field=models.CharField(max_length=3000),
        ),
    ]
