from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from sorl.thumbnail import get_thumbnail

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
	rubrique_principale = models.BooleanField(verbose_name='Catégorie Principale')
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
	categorie = models.ForeignKey(Categories_Article, on_delete=models.PROTECT)
	description = models.TextField()
	image = models.ImageField(upload_to=upload_location_sous_categorie)
	thumbnail_small_size = models.ImageField(upload_to=upload_location_sous_categorie, editable=False)
	thumbnail_middle_size = models.ImageField(upload_to=upload_location_sous_categorie, editable=False)
	prix_min = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Prix de l\'article le plus bas de la catégorie', validators=[MinValueValidator(Decimal('0.01'))]) #Prix d'appel. on doit définir le nombre de digit du champ et après la virgule ==> ici jusqu'à 1 milliard, avec 2 chiffres après la virgule.
	publier = models.BooleanField(verbose_name='Activer / Désactiver la catégorie')
	plats = models.BooleanField(verbose_name='Est une sous-catégorie (type sandwiches dans la catégorie plat)')
	composer = models.BooleanField(verbose_name='Possibilité de composer (cocher) / impossible de composer (vide)')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')

	def save(self, *args, **kwargs):
		self.thumbnail_small_size = get_thumbnail(self.image, '64x64', crop='center', quality=99).name
		self.thumbnail_middle_size = get_thumbnail(self.image, '256x256', crop='center', quality=99).name
		super(Sous_Categories_Article, self).save(*args, **kwargs)

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
class Unite_Oeuvre(models.Model):
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


class Type_Variations_Articles(models.Model):
	nom_type_variation_article = models.CharField(max_length=160, verbose_name='Type de Variations (Bases / Ingrédients / Plats Prêts')
	slug = models.CharField(max_length=160)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')
	
	class Meta:
		verbose_name = 'Type de Variations Articles'
		verbose_name_plural = 'Type de Variations Articles'

	def __unicode__(self):
		return self.nom_type_variation_article

	def __str__(self):
		return self.nom_type_variation_article



class Taux_TVA(models.Model):
	nom_taux_applicable = models.CharField(max_length=160, verbose_name='Taux TVA applicable')
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
	image = models.ImageField(upload_to=upload_location_articles)
	thumbnail_small_size = models.ImageField(upload_to=upload_location_articles, editable=False)
	thumbnail_middle_size = models.ImageField(upload_to=upload_location_articles, editable=False)
	disponible = models.BooleanField(verbose_name='Disponible / Non disponible')
	article_composer = models.BooleanField(verbose_name='Article servant à composer un plat (cocher si oui)')
	sous_categories_articles = models.ForeignKey(Type_Produit, verbose_name='Type d\'article', on_delete=models.PROTECT)
	taux_TVA = models.ForeignKey(Taux_TVA, on_delete=models.PROTECT)
	allergenes = models.ManyToManyField(Allergie, blank=True)
	gluten_info = models.BooleanField(verbose_name='Contient du Gluten: Oui (cocher) / Non (ne pas cocher)')
	vegeterien_info = models.BooleanField(verbose_name='Végéterien friendly: Oui (cocher) / Non (ne pas cocher)')
	type_plat_info = models.BooleanField(verbose_name='Se consomme chaud (cocher) / froid (ne pas cocher)')
	ingredients = models.TextField()
	producteurs = models.ManyToManyField('producteurs.Producteurs', blank=True)
	description = models.TextField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')

	def save(self, *args, **kwargs):
		self.thumbnail_small_size = get_thumbnail(self.image, '64x64', crop='center', quality=99).name
		self.thumbnail_middle_size = get_thumbnail(self.image, '256x256', crop='center', quality=99).name
		super(Article, self).save(*args, **kwargs)
	# prix_unitaire = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	# type_article = models.BooleanField(verbose_name='Si article entrant dans composition plat : Article servant de base (cocher si oui) / Article servant d\'ingrédients (laisser vide)')
	# unite_produit = models.ForeignKey(Unite_Produit)

	class Meta:
		verbose_name = 'Article'
		verbose_name_plural = 'Articles'
		ordering = ['nom', 'timestamp']
		
	def __unicode__(self):
		return self.nom

	def __str__(self):
		return self.nom

class Variations_Articles(models.Model):
	article = models.ForeignKey(Article, on_delete=models.PROTECT)
	nom_article_variation = models.CharField(max_length=160, verbose_name='Nom de la variation de l\'article')
	categories =  models.ForeignKey(Sous_Categories_Article, on_delete=models.PROTECT)
	type_article = models.ForeignKey(Type_Variations_Articles, on_delete=models.PROTECT)
	article_une = models.BooleanField(verbose_name="Article en une? / Cocher si oui.")
	prix_vente_unitaire = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	variation_disponible = models.BooleanField(verbose_name='Variation Disponible / Non disponible')
	unite_oeuvre = models.ForeignKey(Unite_Oeuvre, verbose_name='Unité d\'oeuvre', on_delete=models.PROTECT)
	quantite_mise_en_oeuvre = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	prix_revient = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	producteurs = models.ManyToManyField('producteurs.Producteurs', blank=True)
	stock_disponible = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

	class Meta:
		verbose_name = 'Variation Article'
		verbose_name_plural = 'Variations_Articles Articles'
		ordering = ['nom_article_variation']
		
	def __unicode__(self):
		return self.nom_article_variation

	def __str__(self):
		return self.nom_article_variation	

