# Generated by Django 2.1.2 on 2018-12-15 08:54

import catalogue.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_article_thumbnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='thumbnail',
            new_name='thumbnail_middle_size',
        ),
        migrations.AddField(
            model_name='article',
            name='thumbnail_small_size',
            field=models.ImageField(default=1, editable=False, upload_to=catalogue.models.upload_location_articles),
            preserve_default=False,
        ),
    ]
