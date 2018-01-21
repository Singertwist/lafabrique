from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit
from decimal import Decimal
from django.conf import settings


class Cart(object):
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)

		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def add(self, product, quantity=1):
		product_id = str(product.id)

		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 1,'price': str(product.prix_unitaire)}

		else:
			self.cart[product_id]['quantity'] += quantity #Ajoute +1 à la quantité et met à jour le dictionnaire contenant la quantité. += signifie ajoute à la valeur initiale de quantité.

		self.save()

	def save(self):
		self.session[settings.CART_SESSION_ID] = self.cart
		self.session.modified = True


	def remove(self, product): #Supprimer le produit, quelque soit la quantité.
   		product_id = str(product.id)

   		if product_id in self.cart:
   			del self.cart[product_id]
   		self.save()

	def remove_one(self, product, quantity=1): #Méthode permettant de supprimer une unité du produit.
		product_id = str(product.id)

		if product_id in self.cart: #Si le produit est dans le panier
			if self.cart[product_id]['quantity'] > 1: #Et si la quantité de ce produit est supérieure à 1
				self.cart[product_id]['quantity'] -= quantity #On enlève la quantité par défaut, d'est à dire 1.
			else:
				del self.cart[product_id] #Si la quantité du produit est égale à 1 alors et que l'on veut enlever une unité, cela veut dire que l'on supprimer le produit.
		self.save()


	def __iter__(self):

		product_ids = self.cart.keys() #Sélectionne les différentes clés du dictionnaires, dans notre cas l'id du produit, la quantité, le prix.

		products = Article.objects.filter(id__in=product_ids) #On filtre sur les IDs présents dans le dictionnaire du panier.

		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True
