# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-12 18:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panier', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='panieritem',
            name='article',
        ),
        migrations.DeleteModel(
            name='PanierItem',
        ),
    ]
