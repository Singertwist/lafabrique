# Generated by Django 2.1.2 on 2018-12-13 19:16

import catalogue.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(default=1, editable=False, upload_to=catalogue.models.upload_location_articles),
            preserve_default=False,
        ),
    ]
