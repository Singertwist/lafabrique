from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit
from decimal import Decimal
from django.conf import settings

class Composed_Cart(object):
	def __init__(self, request):
		self.session = request.session
		composed_cart = self.session.get(settings.COMPOSED_CART_SESSION_ID)

		if not composed_cart:
			composed_cart = self.session[settings.COMPOSED_CART_SESSION_ID] = {}
		self.composed_cart = composed_cart

	def add_composed_cart(self, product, quantity=1):
		product_id = str(product.id)

		if product_id not in self.composed_cart:
			self.composed_cart[product_id] = {'quantity': 1,'price': str(product.prix_unitaire), 'tva': str(product.taux_TVA.taux_applicable)}

		else:
			self.composed_cart[product_id]['quantity'] += quantity #Ajoute +1 à la quantité et met à jour le dictionnaire contenant la quantité. += signifie ajoute à la valeur initiale de quantité.

		self.save()

	def save_composed_cart(self):
		self.session[settings.COMPOSED_CART_SESSION_ID] = self.composed_cart
		self.session.modified = True


	def remove_composed_cart(self, product): #Supprimer le produit, quelque soit la quantité.
   		product_id = str(product.id)

   		if product_id in self.composed_cart:
   			del self.composed_cart[product_id]
   		self.save()

	def __iter__(self):

		product_ids = self.composed_cart.keys() #Sélectionne les différentes clés du dictionnaires, dans notre cas l'id du produit, la quantité, le prix.

		products = Article.objects.filter(id__in=product_ids) #On filtre sur les IDs présents dans le dictionnaire du panier.

		for product in products:
			self.composed_cart[str(product.id)]['product'] = product

		for item in self.composed_cart.values():
			item['price'] = Decimal(item['price'])
			item['tva'] = Decimal(item['tva'])
			item['total_price'] = item['price'] * item['quantity']
			item['total_item_tva'] = item['total_price'] - item['total_price'] / item['tva'] #Calcul du total de TVA par article.
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.composed_cart.values())

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.composed_cart.values())

	def get_total_tva(self):
		return sum(round(Decimal(item['total_item_tva']),2) for item in self.composed_cart.values()) #Calcul de la TVA, round(X,2), permet d'arrondir à 2 décimales après la virgule le montant de la TVA

	def get_sub_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.composed_cart.values()) - sum(round(Decimal(item['total_item_tva']),2) for item in self.composed_cart.values())

	def clear(self):
		del self.session[settings.COMPOSED_CART_SESSION_ID]
		self.session.modified = True
