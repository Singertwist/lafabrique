from django.db import models
from catalogue.models import Article
# Create your models here.

class PanierItem(models.Model):
	panier_id = models.CharField(max_length=50)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Date de création')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Date de mise à jour')
	quantite = models.IntegerField(default=1)
	article = models.ForeignKey('catalogue.Article', unique=False)

	class Meta:
		ordering = ['timestamp', 'updated']

	def total(self):
		return self.quantite*self.article.prix_unitaire

	def nom(self):
		return self.article.nom

	def prix(self):
		return self.article.prix_unitaire

	def augment_quantite(self, quantite):
		self.quantite = self.quantite + int(quantite)
		self.save()


