# Generated by Django 2.0.7 on 2018-08-25 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0002_order_montant_commande'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='montant_commande',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
