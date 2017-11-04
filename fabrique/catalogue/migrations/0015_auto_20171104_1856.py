# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0014_auto_20171104_1851'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='prix_unitaire',
            new_name='prix',
        ),
        migrations.RenameField(
            model_name='sous_categories_article',
            old_name='prix_min',
            new_name='prix',
        ),
        migrations.AlterField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(to='catalogue.Sous_Categories_Article'),
        ),
        migrations.AlterField(
            model_name='sous_categories_article',
            name='categorie',
            field=models.ManyToManyField(to='catalogue.Categories_Article'),
        ),
    ]
