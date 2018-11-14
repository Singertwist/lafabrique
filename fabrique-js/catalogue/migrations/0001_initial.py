# Generated by Django 2.0.7 on 2018-08-25 18:25

import catalogue.models
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('producteurs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=160, verbose_name="Nom de l'allergie")),
                ('slug', models.CharField(max_length=160)),
                ('active', models.BooleanField(verbose_name='Actif / Inactif')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
            ],
            options={
                'verbose_name_plural': 'Allergies',
                'verbose_name': 'Allergie',
                'ordering': ['nom', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=160, verbose_name="Nom de l'article")),
                ('slug', models.CharField(max_length=160)),
                ('image', models.ImageField(upload_to=catalogue.models.upload_location_articles)),
                ('disponible', models.BooleanField(verbose_name='Disponible / Non disponible')),
                ('article_composer', models.BooleanField(verbose_name='Article servant à composer un plat (cocher si oui)')),
                ('gluten_info', models.BooleanField(verbose_name='Contient du Gluten: Oui (cocher) / Non (ne pas cocher)')),
                ('vegeterien_info', models.BooleanField(verbose_name='Végéterien friendly: Oui (cocher) / Non (ne pas cocher)')),
                ('type_plat_info', models.BooleanField(verbose_name='Se consomme chaud (cocher) / froid (ne pas cocher)')),
                ('ingredients', models.TextField()),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('allergenes', models.ManyToManyField(blank=True, to='catalogue.Allergie')),
                ('producteurs', models.ManyToManyField(blank=True, to='producteurs.Producteurs')),
            ],
            options={
                'verbose_name_plural': 'Articles',
                'verbose_name': 'Article',
                'ordering': ['nom', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Categories_Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=160, unique=True, verbose_name='Nom de la catégorie')),
                ('slug', models.CharField(max_length=160)),
                ('ordre', models.IntegerField(default=catalogue.models.get_latest_ordre, unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Ordre des rubriques dans le menu')),
                ('rubrique_principale', models.BooleanField(verbose_name='Catégorie Principale')),
                ('actif', models.BooleanField(verbose_name='Actif / Inactif')),
                ('presentation_categorie', models.CharField(max_length=160)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
            ],
            options={
                'verbose_name_plural': 'Catégories Générales',
                'verbose_name': 'Catégorie Générale',
            },
        ),
        migrations.CreateModel(
            name='Sous_Categories_Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=160, verbose_name='Nom de la sous-catégorie')),
                ('slug', models.CharField(max_length=160)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=catalogue.models.upload_location_sous_categorie)),
                ('prix_min', models.DecimalField(decimal_places=2, max_digits=19, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name="Prix de l'article le plus bas de la catégorie")),
                ('publier', models.BooleanField(verbose_name='Activer / Désactiver la catégorie')),
                ('plats', models.BooleanField(verbose_name='Est une sous-catégorie (type sandwiches dans la catégorie plat)')),
                ('composer', models.BooleanField(verbose_name='Possibilité de composer (cocher) / impossible de composer (vide)')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogue.Categories_Article')),
            ],
            options={
                'verbose_name_plural': 'Sous-Catégories des articles',
                'verbose_name': 'Sous-Catégorie des articles',
                'ordering': ['nom', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Taux_TVA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_taux_applicable', models.CharField(max_length=160, verbose_name='Taux TVA applicable')),
                ('taux_applicable', models.DecimalField(decimal_places=2, max_digits=4)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
            ],
            options={
                'verbose_name_plural': 'Taux TVA applicables',
                'verbose_name': 'Taux TVA applicables',
            },
        ),
        migrations.CreateModel(
            name='Type_Produit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=160, verbose_name='Catégorie du produit')),
                ('slug', models.CharField(max_length=160)),
                ('active', models.BooleanField(verbose_name='Actif / Inactif')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
            ],
            options={
                'verbose_name_plural': 'Type du produit',
                'verbose_name': 'Type du produit',
                'ordering': ['nom', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Type_Variations_Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_type_variation_article', models.CharField(max_length=160, verbose_name='Type de Variations (Bases / Ingrédients / Plats Prêts')),
                ('slug', models.CharField(max_length=160)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
            ],
            options={
                'verbose_name_plural': 'Type de Variations Articles',
                'verbose_name': 'Type de Variations Articles',
            },
        ),
        migrations.CreateModel(
            name='Unite_Oeuvre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=160, verbose_name='Unité du produit')),
                ('slug', models.CharField(max_length=160)),
                ('active', models.BooleanField(verbose_name='Actif / Inactif')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
            ],
            options={
                'verbose_name_plural': 'Unité du produit',
                'verbose_name': 'Unité du produit',
                'ordering': ['nom', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Variations_Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_article_variation', models.CharField(max_length=160, verbose_name="Nom de la variation de l'article")),
                ('article_une', models.BooleanField(verbose_name='Article en une? / Cocher si oui.')),
                ('prix_vente_unitaire', models.DecimalField(decimal_places=2, max_digits=19, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('variation_disponible', models.BooleanField(verbose_name='Variation Disponible / Non disponible')),
                ('quantite_mise_en_oeuvre', models.DecimalField(decimal_places=2, max_digits=19, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('prix_revient', models.DecimalField(decimal_places=2, max_digits=19, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('stock_disponible', models.DecimalField(decimal_places=2, max_digits=19, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogue.Article')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogue.Sous_Categories_Article')),
                ('producteurs', models.ManyToManyField(blank=True, to='producteurs.Producteurs')),
                ('type_article', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogue.Type_Variations_Articles')),
                ('unite_oeuvre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogue.Unite_Oeuvre', verbose_name="Unité d'oeuvre")),
            ],
            options={
                'verbose_name_plural': 'Variations_Articles Articles',
                'verbose_name': 'Variation Article',
                'ordering': ['nom_article_variation'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='sous_categories_articles',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogue.Type_Produit', verbose_name="Type d'article"),
        ),
        migrations.AddField(
            model_name='article',
            name='taux_TVA',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogue.Taux_TVA'),
        ),
    ]