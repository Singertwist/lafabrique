# Generated by Django 2.0 on 2018-09-08 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0011_auto_20180908_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='type_product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='catalogue.Sous_Categories_Article', verbose_name='Catégorie Article'),
            preserve_default=False,
        ),
    ]
