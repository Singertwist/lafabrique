from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

# Create your models here.
#Modèle permettant de définir un grande catégorie de plat --> Plats, Desserts, A-côté...
class Categories_Article(models.Model):
	nom = models.CharField(unique=True, max_length=160, verbose_name='Nom de la catégorie')
	slug = models.CharField(max_length=160)
	ordre = models.IntegerField(unique=True, verbose_name='Ordre des rubriques dans le menu')
	actif =  models.BooleanField(verbose_name='Actif / Inactif')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')

	def __unicode__(self):
		return self.nom

	def __str__(self):
		return self.nom

	class Meta:
		verbose_name = 'Catégorie Générale'
		verbose_name_plural = 'Catégories Générales'

#Modèle permettant d'avoir les sous catégories d'articles --> Pour les plats: sandwiches, soupes, salades; Pour les desserts: desserts...
def upload_location_sous_categorie(instance, filename):
	return "photos_sous_categories_articles/%s/%s" %(instance.slug, filename)

class Sous_Categories_Article(models.Model):
	nom = models.CharField(max_length=160, verbose_name='Nom de la sous-catégorie')
	slug = models.CharField(max_length=160)
	categorie = models.ManyToManyField(Categories_Article)
	description = models.TextField()
	image = models.ImageField(upload_to=upload_location_sous_categorie)
	prix_min = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Prix de l\'article le plus bas de la catégorie', validators=[MinValueValidator(Decimal('0.01'))]) #Prix d'appel. on doit définir le nombre de digit du champ et après la virgule ==> ici jusqu'à 1 milliard, avec 2 chiffres après la virgule.
	publier = models.BooleanField(verbose_name='Activer / Désactiver la catégorie')
	plats = models.BooleanField(verbose_name='Fait partie de la rubrique "Plats"')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')

	class Meta:
		verbose_name = 'Sous-Catégorie des articles'
		verbose_name_plural = 'Sous-Catégories des articles'
		ordering = ['nom', 'timestamp']

	def __unicode__(self):
		return self.nom

	def __str__(self):
		return self.nom


#Modèle permettant de définir un article.
def upload_location_articles(instance, filename):
	return "photos_articles/%s/%s" %(instance.slug, filename)

class Article(models.Model):
	nom = models.CharField(max_length=160, verbose_name='Nom de l\'article')
	slug = models.CharField(max_length=160)
	categories =  models.ManyToManyField(Sous_Categories_Article)
	image = models.ImageField(upload_to=upload_location_articles)
	disponible = models.BooleanField(verbose_name='Disponible / Non disponible')
	allergenes = models.TextField()
	gluten_info = models.BooleanField(verbose_name='Contient du Gluten: Oui / Non')
	vegeterien_info = models.BooleanField(verbose_name='Végéterien friendly: Oui / Non')
	ingredients = models.TextField()
	producteurs = models.TextField()
	unite_produit = models.CharField(max_length=160)
	prix_unitaire = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	taux_TVA = models.CharField(max_length=160)
	description = models.TextField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')
	sous_categories_articles = models.CharField(max_length=160)

	class Meta:
		verbose_name = 'Article'
		verbose_name_plural = 'Articles'
		ordering = ['nom', 'timestamp']
		
	def __unicode__(self):
		return self.nom

	def __str__(self):
		return self.nom
