# Generated by Django 2.0.7 on 2018-09-04 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0006_remove_order_picking_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='picking_date',
            field=models.DateTimeField(null=True, verbose_name='Date et Heure de Retrait'),
        ),
    ]
