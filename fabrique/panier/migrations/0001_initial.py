# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-08 21:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PanierItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('panier_id', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('quantite', models.IntegerField(default=1)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Article')),
            ],
            options={
                'ordering': ['timestamp', 'updated'],
            },
        ),
    ]
