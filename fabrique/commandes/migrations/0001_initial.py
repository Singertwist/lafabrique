# Generated by Django 2.0.7 on 2018-07-24 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0012_auto_20180713_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=160, verbose_name='Prénom')),
                ('nom', models.CharField(max_length=160, verbose_name='Nom')),
                ('email', models.EmailField(max_length=254)),
                ('adresse', models.CharField(max_length=250, verbose_name='Adresse')),
                ('code_postal', models.CharField(max_length=5, verbose_name='Code Postal')),
                ('ville', models.CharField(max_length=100, verbose_name='Ville')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('paid', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='commandes.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='catalogue.Variations_Articles')),
            ],
        ),
    ]
