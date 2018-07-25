from django.db import models
from catalogue.models import Article, Variations_Articles
# Create your models here.

class Order(models.Model):
	prenom = models.CharField(max_length=160, verbose_name='Prénom')
	nom = models.CharField(max_length=160, verbose_name='Nom')
	email = models.EmailField()
	adresse = models.CharField(max_length=250, verbose_name='Adresse')
	code_postal = models.CharField(max_length=5, verbose_name='Code Postal')
	ville = models.CharField(max_length=100, verbose_name='Ville')
	created = models.DateTimeField(auto_now_add=True)
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
	product = models.ForeignKey(Variations_Articles, related_name='order_items', on_delete=models.PROTECT)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity





