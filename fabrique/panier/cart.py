from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit
from decimal import Decimal
from django.conf import settings


class Cart(object):
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('cart')
		composed_cart = self.session.get('composed_cart')

		if not cart and not composed_cart:
			cart = self.session['cart'] = {}
			composed_cart = self.session['composed_cart'] = {}
		self.cart = cart
		self.composed_cart = composed_cart	

	def add(self, product, quantity=1):
		product_id = str(product.id)
		if product.article_composer == False:
			if product_id not in self.cart:
				self.cart[product_id] = {'quantity': 1,'price': str(product.prix_unitaire), 'tva': str(product.taux_TVA.taux_applicable)}

			else:
				self.cart[product_id]['quantity'] += quantity #Ajoute +1 à la quantité et met à jour le dictionnaire contenant la quantité. += signifie ajoute à la valeur initiale de quantité.

			self.save()

		else:
			if product_id not in self.composed_cart:
				self.composed_cart[product_id] = {'quantity': 1,'price': str(product.prix_unitaire), 'tva': str(product.taux_TVA.taux_applicable)}

			else:
				self.composed_cart[product_id]['quantity'] += quantity #Ajoute +1 à la quantité et met à jour le dictionnaire contenant la quantité. += signifie ajoute à la valeur initiale de quantité.

			self.save_composed()

	def save(self):
		self.session['cart'] = self.cart
		self.session.modified = True

	def save_composed(self):
		self.session['composed_cart'] = self.composed_cart
		self.session.modified = True

	def remove(self, product): #Supprimer le produit, quelque soit la quantité.
   		product_id = str(product.id)
   		if product.article_composer == False:
	   		if product_id in self.cart:
	   			del self.cart[product_id]
	   		self.save()

	   	else:
	   		if product_id in self.composed_cart:
	   			del self.composed_cart[product_id]
	   		self.save_composed()

	def remove_one(self, product, quantity=1): #Méthode permettant de supprimer une unité du produit.
		product_id = str(product.id)

		if product_id in self.cart: #Si le produit est dans le panier
			if self.cart[product_id]['quantity'] > 1: #Et si la quantité de ce produit est supérieure à 1
				self.cart[product_id]['quantity'] -= quantity #On enlève la quantité par défaut, d'est à dire 1.
			else:
				del self.cart[product_id] #Si la quantité du produit est égale à 1 alors et que l'on veut enlever une unité, cela veut dire que l'on supprimer le produit.
			self.save()
		else: #Si le produit est ajouté dans la composition de plat, on supprime l'article quelque soit la quantité.
			del self.composed_cart[product_id]
			self.save_composed()


	def __iter__(self):

		product_ids = self.cart.keys() #Sélectionne les différentes clés du dictionnaires, dans notre cas l'id du produit, la quantité, le prix.

		products = Article.objects.filter(id__in=product_ids) #On filtre sur les IDs présents dans le dictionnaire du panier.

		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['tva'] = Decimal(item['tva'])
			item['total_price'] = item['price'] * item['quantity']
			item['total_item_tva'] = item['total_price'] - item['total_price'] / item['tva'] #Calcul du total de TVA par article.
			yield item


	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def get_total_tva(self):
		return sum(round(Decimal(item['total_item_tva']),2) for item in self.cart.values()) #Calcul de la TVA, round(X,2), permet d'arrondir à 2 décimales après la virgule le montant de la TVA

	def get_sub_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) - sum(round(Decimal(item['total_item_tva']),2) for item in self.cart.values())

	def clear(self):
		del self.session['cart']
		self.session.modified = True


	#Méthodes spécifiques au panier composable

class ComposedCart(object):
	def __init__(self, request):
		self.session = request.session
		composed_cart = self.session.get('composed_cart')
		self.composed_cart = composed_cart

	def __iter__(self):
		composed_products_ids = self.composed_cart.keys()
		composed_products = Article.objects.filter(id__in=composed_products_ids)

		for composed_product in composed_products:
			self.composed_cart[str(composed_product.id)]['product'] = composed_product

		for composed_item in self.composed_cart.values():
			composed_item['price'] = Decimal(composed_item['price'])
			composed_item['tva'] = Decimal(composed_item['tva'])
			composed_item['total_price'] = composed_item['price'] * composed_item['quantity']
			composed_item['total_composed_item_tva'] = composed_item['total_price'] - composed_item['total_price'] / composed_item['tva'] #Calcul du total de TVA par article.
			yield composed_item

	def __len__(self):
		if not self.composed_cart: #Condition si on arrive directement sur la page de composition d'un plat et qu'il n'y pas de dictionnaire de créé.
			return 0
		else: 
			return sum(composed_item['quantity'] for composed_item in self.composed_cart.values())


