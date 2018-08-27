from django.db import models
from django.core.validators import RegexValidator
from catalogue.models import Article, Variations_Articles, Sous_Categories_Article
# Create your models here.

class Order(models.Model):
	prenom = models.CharField(max_length=160, verbose_name='Prénom')
	nom = models.CharField(max_length=160, verbose_name='Nom')
	email = models.EmailField()
	adresse = models.CharField(max_length=250, verbose_name='Adresse')
	code_postal = models.CharField(max_length=5, verbose_name='Code Postal', validators=[RegexValidator('^(([0-8][0-9])|(9[0-5]))[0-9]{3}$', message="Veuillez renseigner un code postal valide")])
	ville = models.CharField(max_length=100, verbose_name='Ville')
	created = models.DateTimeField(auto_now_add=True)
	montant_commande = models.DecimalField(decimal_places=2, max_digits=10, null=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return 'Order {}'.format(self.id)

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	type_product = models.ForeignKey(Sous_Categories_Article, verbose_name="Catégorie Article", on_delete=models.PROTECT)
	product = models.ManyToManyField(Variations_Articles, max_length=1000, verbose_name='Article')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity



