# Generated by Django 2.1.2 on 2019-04-11 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_auto_20190411_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taux_tva',
            name='taux_applicable',
            field=models.DecimalField(decimal_places=4, max_digits=6),
        ),
    ]
