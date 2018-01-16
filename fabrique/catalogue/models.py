from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
#Modèle permettant de définir un grande catégorie de plat --> Plats, Desserts, A-côté...

#Fonction qui permet d'auto incrémenter l'ordre afin de ne pas à avoir remplir à chaque fois l'ordre et se souvenir du dernier ordre utilisé.
def get_latest_ordre():
	try:
		return Categories_Article.objects.latest('ordre').ordre + 1
	except ObjectDoesNotExist:
		return None

class Categories_Article(models.Model):
	nom = models.CharField(unique=True, max_length=160, verbose_name='Nom de la catégorie')
	slug = models.CharField(max_length=160)
	ordre = models.IntegerField(unique=True, default=get_latest_ordre , validators=[MinValueValidator(1)], verbose_name='Ordre des rubriques dans le menu')
	actif =  models.BooleanField(verbose_name='Actif / Inactif')
	presentation_categorie = models.CharField(max_length=160)
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
	categorie = models.ForeignKey(Categories_Article)
	description = models.TextField()
	image = models.ImageField(upload_to=upload_location_sous_categorie)
	prix_min = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Prix de l\'article le plus bas de la catégorie', validators=[MinValueValidator(Decimal('0.01'))]) #Prix d'appel. on doit définir le nombre de digit du champ et après la virgule ==> ici jusqu'à 1 milliard, avec 2 chiffres après la virgule.
	publier = models.BooleanField(verbose_name='Activer / Désactiver la catégorie')
	plats = models.BooleanField(verbose_name='Est une sous-catégorie (type sandwiches dans la catégorie plat)')
	composer = models.BooleanField(verbose_name='Possibilité de composer (cocher) / impossible de composer (vide)')
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

#Modèle permettant de définir les différents types d'allergie

class Allergie(models.Model):
	nom = models.CharField(max_length=160, verbose_name='Nom de l\'allergie')
	slug = models.CharField(max_length=160)
	active = models.BooleanField(verbose_name='Actif / Inactif')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')

	class Meta:
		verbose_name = 'Allergie'
		verbose_name_plural = 'Allergies'
		ordering = ['nom', 'timestamp']

	def __unicode__(self):
		return self.nom

	def __str__(self):
		return self.nom
#Modèle permettant de définir les différentes unités des articles --> Kilogrammes, Litre, Centilitre, unités
class Unite_Produit(models.Model):
	nom = models.CharField(max_length=160, verbose_name='Unité du produit')
	slug = models.CharField(max_length=160)
	active = models.BooleanField(verbose_name='Actif / Inactif')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')

	class Meta:
		verbose_name = 'Unité du produit'
		verbose_name_plural = 'Unité du produit'
		ordering = ['nom', 'timestamp']

	def __unicode__(self):
		return self.nom

	def __str__(self):
		return self.nom

#Modèle permettant de définir les différentes unités des articles --> Kilogrammes, Litre, Centilitre, unités
class Type_Produit(models.Model):
	nom = models.CharField(max_length=160, verbose_name='Catégorie du produit')
	slug = models.CharField(max_length=160)
	active = models.BooleanField(verbose_name='Actif / Inactif')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')

	class Meta:
		verbose_name = 'Type du produit'
		verbose_name_plural = 'Type du produit'
		ordering = ['nom', 'timestamp']

	def __unicode__(self):
		return self.nom

	def __str__(self):
		return self.nom
class Taux_TVA(models.Model):
	nom_taux_applicable = models.CharField(max_length=160, verbose_name='Taux applicable')
	taux_applicable = models.DecimalField(max_digits=4, decimal_places=2)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')

	class Meta:
		verbose_name = 'Taux TVA applicables'
		verbose_name_plural = 'Taux TVA applicables'

	def __unicode__(self):
		return self.nom_taux_applicable

	def __str__(self):
		return self.nom_taux_applicable
#Modèle permettant de définir un article.
def upload_location_articles(instance, filename):
	return "photos_articles/%s/%s" %(instance.slug, filename)

class Article(models.Model):
	nom = models.CharField(max_length=160, verbose_name='Nom de l\'article')
	slug = models.CharField(max_length=160)
	categories =  models.ManyToManyField(Sous_Categories_Article)
	image = models.ImageField(upload_to=upload_location_articles)
	disponible = models.BooleanField(verbose_name='Disponible / Non disponible')
	article_composer = models.BooleanField(verbose_name='Article servant à composer un plat (cocher si oui)')
	allergenes = models.ManyToManyField(Allergie, blank=True)
	gluten_info = models.BooleanField(verbose_name='Contient du Gluten: Oui (cocher) / Non (ne pas cocher)')
	vegeterien_info = models.BooleanField(verbose_name='Végéterien friendly: Oui (cocher) / Non (ne pas cocher)')
	type_plat_info = models.BooleanField(verbose_name='Se consomme chaud (cocher) / froid (ne pas cocher)')
	ingredients = models.TextField()
	producteurs = models.ManyToManyField('producteurs.Producteurs', blank=True)
	unite_produit = models.ForeignKey(Unite_Produit)
	prix_unitaire = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	taux_TVA = models.ForeignKey(Taux_TVA)
	description = models.TextField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')
	sous_categories_articles = models.ForeignKey(Type_Produit, verbose_name='Type d\'article')

	class Meta:
		verbose_name = 'Article'
		verbose_name_plural = 'Articles'
		ordering = ['nom', 'timestamp']
		
	def __unicode__(self):
		return self.nom

	def __str__(self):
		return self.nom
