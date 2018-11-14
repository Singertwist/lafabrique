from django.db import models

# Create your models here.

class Categories(models.Model):
	categorie_personnes = models.CharField(max_length=160, verbose_name='Catégorie de producteurs / Equipier')
	slug = models.CharField(max_length=160)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')
	actif = models.BooleanField()
	categorie_principale = models.BooleanField(verbose_name='S\'agit-il d\'une catégaorie principale?')
	ordre = models.IntegerField(unique=True)
	description = models.CharField(max_length=160, verbose_name='Présentation de la catégorie de personnes')

	class Meta:
		verbose_name = 'Catégorie personnel / producteur'
		verbose_name_plural = 'Catégories personnel / producteur'
		ordering = ['categorie_personnes', 'timestamp']

	def __unicode__(self):
		return self.categorie_personnes

	def __str__(self):
		return self.categorie_personnes

def upload_location_producteurs(instance, filename):
	return "photos_producteurs/%s" %(filename)

class Producteurs(models.Model):
	nom =  models.CharField(max_length=160, verbose_name='Nom du producteur')
	prenom = models.CharField(max_length=160, verbose_name='Prénom du producteur')
	photo = models.ImageField(upload_to=upload_location_producteurs)
	description = models.TextField(verbose_name='Description du producteur')
	categorie_producteurs = models.ManyToManyField(Categories)
	actif = models.BooleanField()
	rue = models.CharField(max_length=160, verbose_name='Rue du producteur')
	code_postal = models.CharField(max_length=160, verbose_name='Code postal')
	ville = models.CharField(max_length=160, verbose_name='Ville / Localité')
	pays = models.CharField(max_length=160, verbose_name='Pays')
	numero_telephone = models.CharField(max_length=160, verbose_name='N° de Téléphone / de Contact')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')
	afficher_donnees_privees = models.BooleanField()

	class Meta:
		verbose_name = 'Producteur'
		verbose_name_plural = 'Producteurs'

	def __unicode__(self):
		return self.nom

	def __str__(self):
		return self.nom

def upload_location_equipe(instance, filename):
	return "photos_equipe/%s" %(filename)

class Equipes(models.Model):
	nom =  models.CharField(max_length=160, verbose_name='Nom de l\'équipier')
	prenom = models.CharField(max_length=160, verbose_name='Prénom de l\'équipier')
	photo= models.ImageField(upload_to=upload_location_equipe, verbose_name='Photo de l\'équipier')
	categorie_personnel = models.ManyToManyField(Categories)
	description = models.TextField(verbose_name='Description de l\'équipier')
	poste = models.CharField(max_length=160, verbose_name='Poste occupé par l\'équipier')
	actif = models.BooleanField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')
	afficher_donnees_privees = models.BooleanField()

	class Meta:
		verbose_name = 'Equipe'
		verbose_name_plural = 'Equipe'

	def __unicode__(self):
		return self.nom

	def __str__(self):
		return self.nom