# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-11 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producteurs', '0002_remove_categories_ordre'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='ordre',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
