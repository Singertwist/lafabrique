# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 09:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20171105_1049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sous_categories_article',
            name='categorie',
        ),
        migrations.AddField(
            model_name='sous_categories_article',
            name='categorie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalogue.Categories_Article'),
            preserve_default=False,
        ),
    ]
