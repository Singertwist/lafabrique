# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 16:44
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0030_auto_20171203_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='unite_produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Unite_Produit'),
        ),
        migrations.AlterField(
            model_name='categories_article',
            name='ordre',
            field=models.IntegerField(default=1, unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Ordre des rubriques dans le menu'),
        ),
    ]
