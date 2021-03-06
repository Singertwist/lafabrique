# Generated by Django 2.1.2 on 2019-01-01 19:06

import catalogue.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20181215_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='sous_categories_article',
            name='thumbnail_middle_size',
            field=models.ImageField(default=1, editable=False, upload_to=catalogue.models.upload_location_sous_categorie),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sous_categories_article',
            name='thumbnail_small_size',
            field=models.ImageField(default=1, editable=False, upload_to=catalogue.models.upload_location_sous_categorie),
            preserve_default=False,
        ),
    ]
