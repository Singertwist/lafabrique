# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0010_auto_20171101_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(to='catalogue.Sous_Categories_Article'),
        ),
        migrations.AlterField(
            model_name='categories_article',
            name='nom',
            field=models.CharField(max_length=160, unique=True, verbose_name='Nom de la catégorie'),
        ),
        migrations.AlterField(
            model_name='sous_categories_article',
            name='categorie',
            field=models.ManyToManyField(to='catalogue.Categories_Article'),
        ),
    ]