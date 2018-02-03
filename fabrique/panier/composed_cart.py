from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit
from decimal import Decimal
from django.conf import settings

class ComposedCart(object):
	def __init__(self):
		composed_cart = {}
		if not composed_cart:
			composed_cart = {}
		self.composed_cart = composed_cart

	def add(self, product, quantity=1):
		product_id = str(product.id)

		if product_id not in self.composed_cart:
			self.composed_cart[product_id] = {'quantity': 1,'price': str(product.prix_unitaire), 'tva': str(product.taux_TVA.taux_applicable)}

		else:
			self.composed_cart[product_id]['quantity'] += quantity #Ajoute +1 à la quantité et met à jour le dictionnaire contenant la quantité. += signifie ajoute à la valeur initiale de quantité.

		self.save()


	def remove(self, product): #Supprimer le produit, quelque soit la quantité.
   		product_id = str(product.id)

   		if product_id in self.composed_cart:
   			del self.composed_cart[product_id]
   		self.save()

	def __iter__(self):

		product_ids = self.composed_cart.keys() #Sélectionne les différentes clés du dictionnaires, dans notre cas l'id du produit, la quantité, le prix.

		products = Article.objects.filter(id__in=product_ids) #On filtre sur les IDs présents dans le dictionnaire du panier.

		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['tva'] = Decimal(item['tva'])
			item['total_price'] = item['price'] * item['quantity']
			item['total_item_tva'] = item['total_price'] - item['total_price'] / item['tva'] #Calcul du total de TVA par article.
			yield item