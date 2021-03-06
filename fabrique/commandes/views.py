from django.shortcuts import render, get_object_or_404
from panier.cart  import Cart, ComposedCart, FinalComposedCart, CartDataValidation
from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit, Variations_Articles
from .models import Order, OrderItem
from .forms import OrderCreateForm
from django.conf import settings
import stripe
from decimal import Decimal
from django.contrib import messages
import datetime
from django.utils.crypto import get_random_string
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_pk_key = settings.STRIPE_PUBLIC_KEY

def checkout_account(request):
	return render(request, "commandes/checkout-account.html", {})

def order_create(request):
	cart_data_validation = CartDataValidation(request)
	if bool(request.session.get('final_composed_cart')) or bool(request.session.get('cart')): #Condition nécessaire pour afficher si les deux paniers, final_composed_cart et cart sont vides.
		final_composed_cart = FinalComposedCart(request)
		cart = Cart(request)
	else:
		final_composed_cart = None
		cart = None

	if request.method == 'POST':
		if cart != None or final_composed_cart != None: # Condition nécessaire car renvoi une erreur si le panier est vide et que l'on arrive sur la page.Si le panier est vide, cela ne sert à rien de réaliser une requête.
			form = OrderCreateForm(request.POST)
			if form.is_valid():
				# On récupère le montant global de la commande qui est calculé dans le module Panier --> Dernière méthode
				# order = form.save(commit=False) # Nécesessaire pour récupérer une instance de la commande (n° d'id nécessaire pour créer la commande) sans sauvegarder daans la base de données.
				amount = int(final_composed_cart.get_total_ttc_price_general() * 100) # On multiplie par 100 ce montant, car Stripe n'accepte que ces montant entier.
				# Création du numéro de commande à partir de la date du jour
				now = datetime.date.today() # On récupérère la date du jour
				now = now.isoformat() # On convertit en string la date du jour

				order_id = Order.objects.latest('id').id + 1 # Permet de définir le dernier ID utilisé dans la base de données Order. On ajoute +1 pour avoir l'ID actuel
				random_string = get_random_string(3).upper()
				order_id = str(order_id) + "-" + random_string

				try:
					customer = stripe.Charge.create(
						amount = amount,
						currency = "EUR",
						source = form.cleaned_data['stripe_id'],
						description = now + "-" + order_id # On créé le numéro de facture à partir de la date du jour + un tiret + numéri d'ID de la base de données.
						)
					
					order = form.save()

					# Indiquer que la commande est payée
					order.paid = True 
					# Sauvegarde le montant de la commande dans le modèle
					order.montant_commande = final_composed_cart.get_total_ttc_price_general()
					# Sauvegarde du numéro de commande dans la base de données
					order.order_number = now + "-" + str(order.id) + "-" + random_string
					# Sauvegarde de la date et heure de retrait
					order.picking_date = cart_data_validation.picking_date()
					# On sauvegarde le formulaire
					order.save()

					# Création des différents items de la commande
					if cart != None: # Si le panier courant comportant tous les items non composés n'est pas vide, on ajoute les éléments à la base de données.
						for item in cart: # Boucle qui permet de parcourir le dictionnaire contenant les différents éléments de la commande.
							product = OrderItem.objects.create(order=order, type_product=item['cat_name'], price=item['price'], quantity=item['quantity']) # On créé une ligne dans la base de données concernant cette commmande.
							product.product.add(item['product']) # Le champ produit est un ManyToManyField, on ne peut pas utiliser la méthode create, il faut utiliser add : https://stackoverflow.com/questions/50990753/struggling-with-many-to-many-field
						cart.clear()
					if final_composed_cart != None: # SI panier contenant les compositions n'est pas vide, on peut ajouter des éléments à la commande.
						list_items = [] #On créé une liste qui va contenir tous les items d'une composition.
						for item in final_composed_cart: # On créé une boucle qui va parcourir tous les éléments du dictionnaire.
							for key, product in item[1]['items'].items(): # On créé une seconde boucle qui va chercher les éléments de chaque compostion
								list_items.append(product['product']['id']) #On met à jour la liste avec les différents ingrédients de la composition.
							type_product = Sous_Categories_Article.objects.get(id=item[1]['cat_name']['id']) # Nécessaire car on ne peut pas passer directement le paramètre, il faut passer une instance d'où le objects.get.
							list_products = OrderItem.objects.create(order=order, type_product=type_product, price=item[1]['total_ttc_composition_composition'], quantity=item[1]['quantity']) #On créé la ligne de commande dans la base de données avec les informations relatives à la composition.
							list_products.product.add(*list_items) # On ajoute à la ligne de commande les ingrédients de la composition.
							list_items = [] # On vide la liste pour permettre de créer une nouvelle liste avec de nouveaux ingrédients le cas échéant.

						form = OrderCreateForm()
						final_composed_cart.clear()
						return render(request, "commandes/orders-created.html", {'order':order})
				
				except stripe.error.CardError as e:
					form = OrderCreateForm(request.POST) #On recharge la page avec les données renseignées en montrant l'erreur.
					messages.warning(request, e)
					return render(request, "commandes/orders-create.html", {'cart':cart, 'final_composed_cart':final_composed_cart, 'form':form, 'stripe_pk_key':stripe_pk_key, 'cart_data_validation':cart_data_validation})

			else: # Si le formulaire n'est pas valide.
				form = OrderCreateForm(request.POST) #On recharge la page avec les données renseignées en montrant l'erreur.
				return render(request, "commandes/orders-create.html", {'cart':cart, 'final_composed_cart':final_composed_cart, 'form':form, 'stripe_pk_key':stripe_pk_key, 'cart_data_validation':cart_data_validation})
		else:
			form = OrderCreateForm(request.POST)
			messages.warning(request, "<p>Veuillez ajouter quelque chose à votre panier avant de passer à l'étape du paiement.</p>")
			return render(request, "commandes/orders-create.html", {'cart':cart, 'final_composed_cart':final_composed_cart, 'form':form, 'stripe_pk_key':stripe_pk_key, 'cart_data_validation':cart_data_validation})
	
	else:
		form = OrderCreateForm()
		return render(request, "commandes/orders-create.html", {'cart':cart, 'final_composed_cart':final_composed_cart, 'form':form, 'stripe_pk_key':stripe_pk_key, 'cart_data_validation':cart_data_validation})

def order_created(request):
	return render(request, "commandes/orders-create.html", {})

@staff_member_required

def	admin_order_detail(request,	order_id):
	order = get_object_or_404(Order, id=order_id)
	return	render(request, 'admin/commandes/commande/detail.html', {'order':order})