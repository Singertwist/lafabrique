# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 16:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0032_auto_20171203_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='unite_produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Unite_Produit'),
        ),
    ]
