# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-18 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0014_allergie_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='ingredients',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Allergie'),
        ),
    ]
