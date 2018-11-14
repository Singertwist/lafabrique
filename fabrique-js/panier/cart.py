from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit, Variations_Articles
from decimal import Decimal
from django.utils.crypto import get_random_string
from django.conf import settings
import datetime
import simplejson as json
from django.forms.models import model_to_dict

class Cart(object):
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('cart')
		composed_cart = self.session.get('composed_cart')
		final_composed_cart = self.session.get('final_composed_cart')
		cart_data_validation = self.session.get('cart_data_validation')

		if not cart and not composed_cart and not final_composed_cart and not cart_data_validation:
			cart = self.session['cart'] = {}
			composed_cart = self.session['composed_cart'] = {}
			final_composed_cart = self.session['final_composed_cart'] = {}
			cart_data_validation = self.session['cart_data_validation'] = {}
		self.cart = cart
		self.composed_cart = composed_cart
		self.final_composed_cart = final_composed_cart
		self.cart_data_validation = cart_data_validation

	def add(self, product, quantity=1):
		product_id = str(product.id)
		if product.article.article_composer == False:
			if product_id not in self.cart:
				self.cart[product_id] = {'quantity': 1,'price': str(product.prix_vente_unitaire), 'tva': str(product.article.taux_TVA.taux_applicable)}

			else:
				self.cart[product_id]['quantity'] += quantity #Ajoute +1 à la quantité et met à jour le dictionnaire contenant la quantité. += signifie ajoute à la valeur initiale de quantité.

			self.save()

		else:
			if sum(composed_item['base'] == "Bases" for composed_item in self.composed_cart.values()) == 1 and str(product.type_article) == "Bases": #On compte le nombre de fois qu'il y a de base dans la composition. S'il y a aucune base on peut ajouter une base. S'il y a une base et que l'article que l'on veut un article qui est une base alors on ne peut pas.
				return "Only_one_base"
			else:
				if product_id not in self.composed_cart:
					self.composed_cart[product_id] = {'quantity': 1,'price': str(product.prix_vente_unitaire), 'tva': str(product.article.taux_TVA.taux_applicable), 'base': str(product.type_article)}

				else:
					return "Same_articles" # Si l'article est déjà présent dans le panier composition, retourne un message d'erreur.
					#self.composed_cart[product_id]['quantity'] += quantity #Ajoute +1 à la quantité et met à jour le dictionnaire contenant la quantité. += signifie ajoute à la valeur initiale de quantité.
				self.save_composed()

	def save(self):
		self.session['cart'] = self.cart
		self.session.modified = True

	def save_composed(self):
		self.session['composed_cart'] = self.composed_cart
		self.session.modified = True

	def remove(self, product): #Supprimer le produit, quelque soit la quantité.
   		product_id = str(product.id)
   		if product.article.article_composer == False:
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

		products = Variations_Articles.objects.filter(id__in=product_ids) #On filtre sur les IDs présents dans le dictionnaire du panier.

		for product in products:
			self.cart[str(product.id)]['product'] = product
			self.cart[str(product.id)]['cat_name'] = product.categories

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
		self.cart = {}
		self.save()

# Méthodes spécifiques au panier composable

class ComposedCart(object):
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('cart')
		composed_cart = self.session.get('composed_cart')
		final_composed_cart = self.session.get('final_composed_cart')
		cart_data_validation = self.session.get('cart_data_validation')

		if not cart and not composed_cart and not final_composed_cart and not cart_data_validation:
			cart = self.session['cart'] = {}
			composed_cart = self.session['composed_cart'] = {}
			final_composed_cart = self.session['final_composed_cart'] = {}
			cart_data_validation = self.session['cart_data_validation'] = {}
		self.cart = cart
		self.composed_cart = composed_cart
		self.final_composed_cart = final_composed_cart
		self.cart_data_validation = cart_data_validation

	def remove_composed_cart(self, categorie_composed_cart):
		self.composed_cart = {}
		self.save_composed()

	def save_composed(self):
		self.session['composed_cart'] = self.composed_cart
		self.session.modified = True

	def __iter__(self):
		if self.composed_cart != None: #Ajouter si vide et que l'on supprime les cookies, sinon cela génère des erreurs. Génère une erreur avec l'ajout du code pour regrouper les différents éléments dans la composition.
			composed_products_ids = self.composed_cart.keys()
			composed_products = Variations_Articles.objects.filter(id__in=composed_products_ids)

			for composed_product in composed_products:
				self.composed_cart[str(composed_product.id)]['product'] = composed_product

			for composed_item in self.composed_cart.values():
				composed_item['price'] = json.dumps(Decimal(composed_item['price']))
				composed_item['tva'] = json.dumps(Decimal(composed_item['tva']))
				composed_item['total_price'] = json.dumps(Decimal(composed_item['price']) * composed_item['quantity'])
				composed_item['total_composed_item_tva'] = json.dumps(Decimal(composed_item['total_price']) - Decimal(composed_item['total_price']) / Decimal(composed_item['tva'])) #Calcul du total de TVA par article.
				yield composed_item

	def __len__(self):
		return sum(composed_item['quantity'] for composed_item in self.composed_cart.values())

class FinalComposedCart(object):
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('cart')
		composed_cart = self.session.get('composed_cart')
		final_composed_cart = self.session.get('final_composed_cart')
		cart_data_validation = self.session.get('cart_data_validation')

		if not cart and not composed_cart and not final_composed_cart and not cart_data_validation:
			cart = self.session['cart'] = {}
			composed_cart = self.session['composed_cart'] = {}
			final_composed_cart = self.session['final_composed_cart'] = {}
			cart_data_validation = self.session['cart_data_validation'] = {}
		self.cart = cart
		self.composed_cart = composed_cart
		self.final_composed_cart = final_composed_cart
		self.cart_data_validation = cart_data_validation

	def add_to_final_composed_cart(self, categorie_composed_cart, comment, quantity=1):
		if sum(composed_item['quantity'] for composed_item in self.composed_cart.values()) > 1: # Condition empêchant l'ajout d'une composition au panier final si le panier composé est vide. Permet de s'assurer que la quantité est supérieur à 1 dans la panier composé.
			if sum(composed_item['base'] == "Bases" for composed_item in self.composed_cart.values()) == 1: #Condition qui empêche d'ajouter une composition au panier final s'il n'y a pas au mois une base. COmpte le nombre de base dans le dictionnaire.
				composed_cart_id = get_random_string(50) + str(datetime.datetime.now()) # Permet de définir un ID pour chaque plat composé.
				composed_cart_id = composed_cart_id.replace(" ", "") #Supprimer tous les espaces de la chaine de caractère.
				categorie_composed_cart_id = str(categorie_composed_cart.id) # Permet de récupérer la catégorie du plat composé (sandwiches, soupe, salade).
				comment = str(comment)

				self.final_composed_cart[composed_cart_id] = {'cat_composed_cart':categorie_composed_cart_id, 'quantity': 1, 'comment': comment, 'items':self.composed_cart}
				self.save_final_composed()
				self.composed_cart = {}
				self.save_composed()
				return "Sucess"
			else:
				return "Zero_quantity"
		else:
				return "Zero_quantity"

	def remove_final_composed_cart(self, dict_key): #Supprimer la composition, quelque soit la quantité.
   		dict_key = str(dict_key)
	   	if dict_key in self.final_composed_cart:
   			del self.final_composed_cart[dict_key]
   		self.save_final_composed()

	def add_quantity_final_composed_cart(self, dict_key, quantity=1):
   		dict_key = str(dict_key)
   		if dict_key in self.final_composed_cart:
   			self.final_composed_cart[dict_key]['quantity'] += quantity
   		self.save_final_composed()

	def remove_one_quantity_final_composed_cart(self, dict_key, quantity=1):
   		dict_key = str(dict_key)
   		if dict_key in self.final_composed_cart:
   			if self.final_composed_cart[dict_key]['quantity'] > 1:
   				self.final_composed_cart[dict_key]['quantity'] -= quantity
   			else:
   				del self.final_composed_cart[dict_key]
   		self.save_final_composed()

	def cart_modify_final_composed_cart(self, dict_key): # Fonction permettant de modifier la composition d'un panier
   		dict_key = str(dict_key) # On récupère la clé du dictionnaire.
   		if dict_key in self.final_composed_cart: # Si la clé correspond à une présente dans le dictionnaire
   			self.composed_cart = {} # Je vide le dictionnaire permettant de composer un panier
   			self.composed_cart.update(self.final_composed_cart[dict_key]['items']) # Je mets à jour le dictionnaire permettant de composer un panier avec les infos de la compostion à modifier et présente dans le panier final.
   			del self.final_composed_cart[dict_key] # Je supprime la composition du panier final car je vais la modifier. Cette composition sera de nouveau validée et donc présente dans le panier final.
   		self.save_composed()
   		self.save_final_composed()

	def save_final_composed(self):
		self.session['final_composed_cart'] = self.final_composed_cart
		self.session.modified = True

	def save_composed(self):
		self.session['composed_cart'] = self.composed_cart
		self.session.modified = True

	def clear(self):
		self.final_composed_cart = {}
		self.save_final_composed()

	def __iter__(self):
		# Extraction des articles des différentes compositions #
		final_composed_product_ids = [] #Création d'une liste pour récupérer tous les ids des articles servant à composer un panier
		for i in self.final_composed_cart: #Pour toutes les compositions
			for k in self.final_composed_cart[i]['items'].keys(): #On récupére les ID des articles
				final_composed_product_ids.append(k) #On met à jour la liste avec append afin de ne pas écraser les informations ajoutées précédemment.

		final_composed_products = Variations_Articles.objects.filter(id__in=final_composed_product_ids) #On peut extraire alors tous les articles avec et les stocker dans la variable

		#Itération pour insérer le nom du produit dans le dictionnaire de la composition.
		for i in self.final_composed_cart: # Pour toutes les compositions créées.
			for final_composed_products_dict_ids in self.final_composed_cart[i]['items'].keys(): #On sélectionne dans un dictionnaire les IDs des différents articles ajoutés.
				for final_composed_product in final_composed_products: # Pour chaque article présent dans la Queryset des différents articles
					if str(final_composed_product.id) in final_composed_products_dict_ids: # Si l'ID de mon article est présent dans le dictionnaire d'ID
						self.final_composed_cart[i]['items'][str(final_composed_products_dict_ids)]['product'] = model_to_dict(final_composed_product, fields=['id', 'nom_article_variation']) #Alors je peux ajouter le nom de l'article dans un clé "produit". Information concernant la sérialisation d'objet (Queryset) https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact

		# Extraction des catégories de chaque composition #
		final_composed_cat_ids = [] # Création d'une liste pour récupérer les ID de chaque catégorie de compositions
		for k in self.final_composed_cart.keys(): #On parcourt le dictionnaire des composition
			final_composed_cat_ids.append(self.final_composed_cart[k]['cat_composed_cart']) #Pour chaque composition, on isole l'ID correspondant à la catégorie de la composition (sandwiches composés, soupes composées...).

		final_composed_cats = Sous_Categories_Article.objects.filter(id__in=final_composed_cat_ids) #On récupère les données dans la base de données concernant ces catégories.

		#Itération pour insérer le nom de la catégorie dans le dictionnaire de la composition.
		for k in self.final_composed_cart.keys():
			for final_composed_cart_cats_id in self.final_composed_cart[k]['cat_composed_cart']:
				for final_composed_cat in final_composed_cats:
					if str(final_composed_cat.id) in final_composed_cart_cats_id:
						self.final_composed_cart[k]['cat_name'] = model_to_dict(final_composed_cat, fields=['id', 'nom', str('image')]) #Information concernant la sérialisation d'objet (Queryset) https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact

		# Mise en forme du dictionnaires Items
		for k in self.final_composed_cart.keys():
			# final_composed_cat = self.final_composed_cart[k]['cat_name']	
			# yield final_composed_cat
			for final_composed_item in self.final_composed_cart[k]['items'].values():
				final_composed_item['price'] = json.dumps(Decimal(final_composed_item['price'])) # Information concernant la sérialization de Decimal https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
				final_composed_item['tva'] = json.dumps(Decimal(final_composed_item['tva']))
				final_composed_item['total_price'] = json.dumps(Decimal(final_composed_item['price']) * Decimal(final_composed_item['quantity']))
				final_composed_item['total_composed_item_tva'] = json.dumps(Decimal(final_composed_item['total_price']) - Decimal(final_composed_item['total_price']) / Decimal(final_composed_item['tva']), use_decimal=True)
				# yield final_composed_item

		# Calcul des totaux pour chaque composition (tva...)
		total_ttc_composition_final = 0 # Déclaration de la variable
		total_tva_composition_final = 0 # Déclaration de la variable
		for k in self.final_composed_cart.keys():
			for final_composed_item in self.final_composed_cart[k]['items'].values():
				total_ttc_composition_final += Decimal(final_composed_item['total_price']) # On additionne tous les valeurs de total_price pour chaque dictionnaire items
				total_tva_composition_final += Decimal(final_composed_item['total_composed_item_tva']) # On additionne tous les valeurs de total_tva pour chaque dictionnaire items
			self.final_composed_cart[k]['total_ttc_composition_composition'] = json.dumps(round(Decimal(total_ttc_composition_final * self.final_composed_cart[k]['quantity']),2))# On insère le total calculé dans le dictionnaire que l'on multiplie par la quantité dans la composition
			self.final_composed_cart[k]['total_tva_composition_final'] = json.dumps(round(Decimal(total_tva_composition_final * self.final_composed_cart[k]['quantity']),2)) # On insère le total calculé dans le dictionnaire
			self.final_composed_cart[k]['total_ht_composition_final'] = json.dumps(round((Decimal(total_ttc_composition_final) - Decimal(total_tva_composition_final)) * self.final_composed_cart[k]['quantity'],2)) # On calcule et n insère le total calculé dans le dictionnaire
			total_ttc_composition_final = 0 # On réiniialise la valeur pour recommencer le cumul à zéro.
			total_tva_composition_final = 0 # On réiniialise la valeur pour recommencer le cumul à zéro.

		# Début de la boucle d'itération #
		for final_composition_items in self.final_composed_cart.items(): # On boucle sur toutes les valeurs du dictionnaire.
			yield final_composition_items	# Boucle avec yield nécessaire pour afficher les valeurs

	def get_total_tva_composed(self):
		return sum(Decimal(v['total_tva_composition_final']) for v in self.final_composed_cart.values())

	def get_total_ttc_price_composed(self):
		return sum(Decimal(v['total_ttc_composition_composition']) for v in self.final_composed_cart.values())

	def get_total_ht_composed(self):
		return sum(Decimal(v['total_ttc_composition_composition']) for v in self.final_composed_cart.values()) - sum(Decimal(v['total_tva_composition_final']) for v in self.final_composed_cart.values())

# Début du calcul général. Il est nécessaire d'ajouter le calcul des boucles à chaque méthode. Si on n'ajoute pas les ces boucles les clés pour calculer les différents totaux ne fonctionnent pas.
	def get_total_tva_general(self):
		for k in self.final_composed_cart.keys():
			# final_composed_cat = self.final_composed_cart[k]['cat_name']	
			# yield final_composed_cat
			for final_composed_item in self.final_composed_cart[k]['items'].values():
				final_composed_item['price'] = Decimal(final_composed_item['price'])
				final_composed_item['tva'] = Decimal(final_composed_item['tva'])
				final_composed_item['total_price'] = final_composed_item['price'] * final_composed_item['quantity']
				final_composed_item['total_composed_item_tva'] = final_composed_item['total_price'] - final_composed_item['total_price'] / final_composed_item['tva']
				# yield final_composed_item

		# Calcul des totaux pour chaque composition (tva...)
		total_ttc_composition_final = 0 # Déclaration de la variable
		total_tva_composition_final = 0 # Déclaration de la variable
		for k in self.final_composed_cart.keys():
			for final_composed_item in self.final_composed_cart[k]['items'].values():
				total_ttc_composition_final += final_composed_item['total_price'] # On additionne tous les valeurs de total_price pour chaque dictionnaire items
				total_tva_composition_final += final_composed_item['total_composed_item_tva'] # On additionne tous les valeurs de total_tva pour chaque dictionnaire items
			self.final_composed_cart[k]['total_ttc_composition_composition'] = total_ttc_composition_final * self.final_composed_cart[k]['quantity']# On insère le total calculé dans le dictionnaire que l'on multiplie par la quantité dans la composition
			self.final_composed_cart[k]['total_tva_composition_final'] = total_tva_composition_final * self.final_composed_cart[k]['quantity'] # On insère le total calculé dans le dictionnaire
			self.final_composed_cart[k]['total_ht_composition_final'] = (total_ttc_composition_final - total_tva_composition_final) * self.final_composed_cart[k]['quantity'] # On calcule et n insère le total calculé dans le dictionnaire
			total_ttc_composition_final = 0 # On réiniialise la valeur pour recommencer le cumul à zéro.
			total_tva_composition_final = 0 # On réiniialise la valeur pour recommencer le cumul à zéro.
		return round(sum(Decimal(v['total_tva_composition_final']) for v in self.final_composed_cart.values()) + sum(round(Decimal(item['total_item_tva']),2) for item in self.cart.values()),2)

	def get_total_ttc_price_general(self):
		for k in self.final_composed_cart.keys():
			# final_composed_cat = self.final_composed_cart[k]['cat_name']	
			# yield final_composed_cat
			for final_composed_item in self.final_composed_cart[k]['items'].values():
				final_composed_item['price'] = Decimal(final_composed_item['price'])
				final_composed_item['tva'] = Decimal(final_composed_item['tva'])
				final_composed_item['total_price'] = final_composed_item['price'] * final_composed_item['quantity']
				final_composed_item['total_composed_item_tva'] = final_composed_item['total_price'] - final_composed_item['total_price'] / final_composed_item['tva']
				# yield final_composed_item

		# Calcul des totaux pour chaque composition (tva...)
		total_ttc_composition_final = 0 # Déclaration de la variable
		total_tva_composition_final = 0 # Déclaration de la variable
		for k in self.final_composed_cart.keys():
			for final_composed_item in self.final_composed_cart[k]['items'].values():
				total_ttc_composition_final += final_composed_item['total_price'] # On additionne tous les valeurs de total_price pour chaque dictionnaire items
				total_tva_composition_final += final_composed_item['total_composed_item_tva'] # On additionne tous les valeurs de total_tva pour chaque dictionnaire items
			self.final_composed_cart[k]['total_ttc_composition_composition'] = round(Decimal(total_ttc_composition_final * self.final_composed_cart[k]['quantity']),2)# On insère le total calculé dans le dictionnaire que l'on multiplie par la quantité dans la composition
			self.final_composed_cart[k]['total_tva_composition_final'] = round(Decimal(total_tva_composition_final * self.final_composed_cart[k]['quantity']),2) # On insère le total calculé dans le dictionnaire
			self.final_composed_cart[k]['total_ht_composition_final'] = round(Decimal((total_ttc_composition_final - total_tva_composition_final) * self.final_composed_cart[k]['quantity']),2) # On calcule et n insère le total calculé dans le dictionnaire
			total_ttc_composition_final = 0 # On réiniialise la valeur pour recommencer le cumul à zéro.
			total_tva_composition_final = 0 # On réiniialise la valeur pour recommencer le cumul à zéro.
		
		return sum(Decimal(v['total_ttc_composition_composition']) for v in self.final_composed_cart.values()) + sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def get_total_ht_price_general(self):
		for k in self.final_composed_cart.keys():
			# final_composed_cat = self.final_composed_cart[k]['cat_name']	
			# yield final_composed_cat
			for final_composed_item in self.final_composed_cart[k]['items'].values():
				final_composed_item['price'] = Decimal(final_composed_item['price'])
				final_composed_item['tva'] = Decimal(final_composed_item['tva'])
				final_composed_item['total_price'] = final_composed_item['price'] * final_composed_item['quantity']
				final_composed_item['total_composed_item_tva'] = final_composed_item['total_price'] - final_composed_item['total_price'] / final_composed_item['tva']
				# yield final_composed_item

		# Calcul des totaux pour chaque composition (tva...)
		total_ttc_composition_final = 0 # Déclaration de la variable
		total_tva_composition_final = 0 # Déclaration de la variable
		for k in self.final_composed_cart.keys():
			for final_composed_item in self.final_composed_cart[k]['items'].values():
				total_ttc_composition_final += final_composed_item['total_price'] # On additionne tous les valeurs de total_price pour chaque dictionnaire items
				total_tva_composition_final += final_composed_item['total_composed_item_tva'] # On additionne tous les valeurs de total_tva pour chaque dictionnaire items
			self.final_composed_cart[k]['total_ttc_composition_composition'] = total_ttc_composition_final * self.final_composed_cart[k]['quantity']# On insère le total calculé dans le dictionnaire que l'on multiplie par la quantité dans la composition
			self.final_composed_cart[k]['total_tva_composition_final'] = total_tva_composition_final * self.final_composed_cart[k]['quantity'] # On insère le total calculé dans le dictionnaire
			self.final_composed_cart[k]['total_ht_composition_final'] = (total_ttc_composition_final - total_tva_composition_final) * self.final_composed_cart[k]['quantity'] # On calcule et n insère le total calculé dans le dictionnaire
			total_ttc_composition_final = 0 # On réiniialise la valeur pour recommencer le cumul à zéro.
			total_tva_composition_final = 0 # On réiniialise la valeur pour recommencer le cumul à zéro.
		return sum(Decimal(v['total_ttc_composition_composition']) for v in self.final_composed_cart.values()) + sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) - round(sum(Decimal(v['total_tva_composition_final']) for v in self.final_composed_cart.values()) + sum(round(Decimal(item['total_item_tva']),2) for item in self.cart.values()),2)

class CartDataValidation(object):
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('cart')
		composed_cart = self.session.get('composed_cart')
		final_composed_cart = self.session.get('final_composed_cart')
		cart_data_validation = self.session.get('cart_data_validation')

		if not cart and not composed_cart and not final_composed_cart and not cart_data_validation:
			cart = self.session['cart'] = {}
			composed_cart = self.session['composed_cart'] = {}
			final_composed_cart = self.session['final_composed_cart'] = {}
			cart_data_validation = self.session['cart_data_validation'] = {}
		self.cart = cart
		self.composed_cart = composed_cart
		self.final_composed_cart = final_composed_cart
		self.cart_data_validation = cart_data_validation		

	def add_date(self, date):
		date = str(date)
		if date not in self.cart:
			self.cart_data_validation['date'] = {'picking_date': date}

		self.save()

	def save(self):
		self.session['cart_data_validation'] = self.cart_data_validation
		self.session.modified = True

	def __iter__(self):
		for data in self.cart_data_validation.values():
			data['date'] = datetime.datetime.strptime(data['picking_date'][:19], "%Y-%m-%d %H:%M:%S").date() # Pour info: https://stackoverflow.com/questions/36753868/python-convert-dictionary-of-string-times-to-date-times
			data['time'] = datetime.datetime.strptime(data['picking_date'][:19], "%Y-%m-%d %H:%M:%S").time() # Pour info suite https://stackoverflow.com/questions/18039680/django-get-only-date-from-datetime-strptime
			yield data

	def picking_date(self):
		for data in self.cart_data_validation.values():
			data['datetime'] = data['picking_date']
		return data['datetime']

	def clear(self):
		self.cart_data_validation = {}
		self.save()
	# if bool(self.final_composed_cart) is True: # Condition qui vérifie si le dictionnaire est vide, s'il est vide, renvoi des dictionnaire vide.
		# 	for i in self.final_composed_cart: #Pour chaque composition présent dans le panier contenant toutes les compositions
		# 		final_composed_product_ids = self.final_composed_cart[i]['items'].keys() # On extrait les ID des articles du dictionnaire item (contenant les différents articles de la composition).
		# 		final_composed_items = self.final_composed_cart[i]['items'].values() # On extrait également les valeurs relatives à ces articles.
		# 		final_composed_dict = self.final_composed_cart[i]['items']
		# else:
		# 	final_composed_product_ids = {}
		# 	final_composed_items = {}
		# 	final_composed_dict = {}

		# final_composed_products_dict = {}
		# for i in self.final_composed_cart:
		# 	final_composed_products_dict.update(self.final_composed_cart[i]['items'])

		# for final_composed_product in final_composed_products:
		# 	final_composed_products_dict[str(final_composed_product.id)]['product'] = final_composed_product

		# for k, v in self.final_composed_cart.items():
		# 	final_composed_cat = self.final_composed_cart[k]['cat_composed_cart']
		# 	final_composed_items = self.final_composed_cart[k]['items'].values()
		# 	yield final_composed_cat, final_composed_items

		# final_composed_products = Article.objects.filter(id__in=final_composed_product_ids)
		# final_composed_cats = Sous_Categories_Article.objects.filter(id__in=final_composed_product_ids)
		
		# for final_composed_product in final_composed_products:
		#  	final_composed_dict[str(final_composed_product.id)]['product'] = final_composed_product
				
		# for k, v in self.final_composed_cart.items():
		# 	k, v
		# 	yield k, v

		# for composition in self.final_composed_cart.keys():
		# 	final_composed_cat = self.final_composed_cart[composition]['cat_composed_cart']
		# 	yield final_composed_cat

		# for k in self.final_composed_cart.keys():
		# 	final_composed_cat = self.final_composed_cart[k]['cat_composed_cart']
		# 	yield final_composed_cat


		# for composition in self.final_composed_cart:
		# 	for final_composed_item in final_composed_items:
		# 		final_composed_item['price'] = Decimal(final_composed_item['price'])
		# 		final_composed_item['tva'] = Decimal(final_composed_item['tva'])
		# 		final_composed_item['total_price'] = final_composed_item['price'] * final_composed_item['quantity']
		# 		final_composed_item['total_composed_item_tva'] = final_composed_item['total_price'] - final_composed_item['total_price'] / final_composed_item['tva'] #Calcul du total de TVA par article.
		# 		yield final_composed_item
		# 	yield composition

