# Generated by Django 2.0.7 on 2018-08-25 18:25

from django.db import migrations, models
import producteurs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorie_personnes', models.CharField(max_length=160, verbose_name='Catégorie de producteurs / Equipier')),
                ('slug', models.CharField(max_length=160)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('actif', models.BooleanField()),
                ('categorie_principale', models.BooleanField(verbose_name="S'agit-il d'une catégaorie principale?")),
                ('ordre', models.IntegerField(unique=True)),
                ('description', models.CharField(max_length=160, verbose_name='Présentation de la catégorie de personnes')),
            ],
            options={
                'verbose_name_plural': 'Catégories personnel / producteur',
                'verbose_name': 'Catégorie personnel / producteur',
                'ordering': ['categorie_personnes', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Equipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=160, verbose_name="Nom de l'équipier")),
                ('prenom', models.CharField(max_length=160, verbose_name="Prénom de l'équipier")),
                ('photo', models.ImageField(upload_to=producteurs.models.upload_location_equipe, verbose_name="Photo de l'équipier")),
                ('description', models.TextField(verbose_name="Description de l'équipier")),
                ('poste', models.CharField(max_length=160, verbose_name="Poste occupé par l'équipier")),
                ('actif', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('afficher_donnees_privees', models.BooleanField()),
                ('categorie_personnel', models.ManyToManyField(to='producteurs.Categories')),
            ],
            options={
                'verbose_name_plural': 'Equipe',
                'verbose_name': 'Equipe',
            },
        ),
        migrations.CreateModel(
            name='Producteurs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=160, verbose_name='Nom du producteur')),
                ('prenom', models.CharField(max_length=160, verbose_name='Prénom du producteur')),
                ('photo', models.ImageField(upload_to=producteurs.models.upload_location_producteurs)),
                ('description', models.TextField(verbose_name='Description du producteur')),
                ('actif', models.BooleanField()),
                ('rue', models.CharField(max_length=160, verbose_name='Rue du producteur')),
                ('code_postal', models.CharField(max_length=160, verbose_name='Code postal')),
                ('ville', models.CharField(max_length=160, verbose_name='Ville / Localité')),
                ('pays', models.CharField(max_length=160, verbose_name='Pays')),
                ('numero_telephone', models.CharField(max_length=160, verbose_name='N° de Téléphone / de Contact')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('afficher_donnees_privees', models.BooleanField()),
                ('categorie_producteurs', models.ManyToManyField(to='producteurs.Categories')),
            ],
            options={
                'verbose_name_plural': 'Producteurs',
                'verbose_name': 'Producteur',
            },
        ),
    ]
