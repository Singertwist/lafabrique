# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-18 10:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producteurs', '0004_auto_20180318_1146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producteurs',
            old_name='afficher_donnees_privee',
            new_name='afficher_donnees_privees',
        ),
    ]