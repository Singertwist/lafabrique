# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 19:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0020_auto_20171119_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type_Produit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=160, verbose_name="Nom de l'allergie")),
                ('slug', models.CharField(max_length=160)),
                ('active', models.BooleanField(verbose_name='Actif / Inactif')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
            ],
            options={
                'verbose_name': 'Type du produit',
                'verbose_name_plural': 'Type du produit',
                'ordering': ['nom', 'timestamp'],
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='sous_categories_articles',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Type_Produit'),
        ),
        migrations.AlterField(
            model_name='article',
            name='unite_produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Unite_Produit'),
        ),
    ]
