# Generated by Django 2.0.7 on 2018-08-27 20:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0003_auto_20180825_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=160, null=True, verbose_name='Numéro de Commande'),
        ),
        migrations.AlterField(
            model_name='order',
            name='code_postal',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^(([0-8][0-9])|(9[0-5]))[0-9]{3}$', message='Veuillez renseigner un code postal valide')], verbose_name='Code Postal'),
        ),
    ]