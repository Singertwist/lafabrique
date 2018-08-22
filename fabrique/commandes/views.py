from django.shortcuts import render
from panier.cart  import Cart, ComposedCart, FinalComposedCart
from .models import Order, OrderItem
from .forms import OrderCreateForm
from django.conf import settings
import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_PUBLIC_KEY

def checkout_account(request):
	return render(request, "commandes/checkout-account.html", {})

def order_create(request):
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
				order = form.save()
				if cart != None: # Si le panier courant comportant tous les items non composés n'est pas vide, on ajoute les éléments à la base de données.
					for item in cart: # Boucle qui permet de parcourir le dictionnaire contenant les différents éléments de la commande.
						product = OrderItem.objects.create(order=order, type_product=item['cat_name'], price=item['price'], quantity=item['quantity']) # On créé une ligne dans la base de données concernant cette commmande.
						product.product.add(item['product']) # Le champ produit est un ManyToManyField, on ne peut pas utiliser la méthode create, il faut utiliser add : https://stackoverflow.com/questions/50990753/struggling-with-many-to-many-field
				if final_composed_cart != None: # SI panier contenant les compositions n'est pas vide, on peut ajouter des éléments à la commande.
					list_items = [] #On créé une liste qui va contenir tous les items d'une composition.
					for item in final_composed_cart: # On créé une boucle qui va parcourir tous les éléments du dictionnaire.
						for key, product in item[1]['items'].items(): # On créé une seconde boucle qui va chercher les éléments de chaque compostion
							list_items.append(product['product']) #On met à jour la liste avec les différents ingrédients de la composition.
						# OrderTypeItem.objects.create(order=order, type_product=item[1]['cat_name'], product=list_items, price=item[1]['total_ttc_composition_composition'], quantity=item[1]['quantity'])
						list_products = OrderItem.objects.create(order=order, type_product=item[1]['cat_name'], price=item[1]['total_ttc_composition_composition'], quantity=item[1]['quantity']) #On créé la ligne de commande dans la base de données avec les informations relatives à la composition.
						list_products.product.add(*list_items) # On ajoute à la ligne de commande les ingrédients de la composition.
						list_items = [] # On vide la liste pour permettre de créer une nouvelle liste avec de nouveaux ingrédients le cas échéant.

			# try:
			# 	customer = stripe.Charge.create(
			# 		amount = 499,
			# 		currency = "eur",
			# 		description = 'Example',
			# 		card = form.cleaned_data['stripe_id'],
			# 		)

				form = OrderCreateForm()
				cart.clear() and final_composed_cart.clear()
				return render(request, "commandes/orders-created.html", {'order':order})

			# except stripe.CardError as e:
			# 	messages.warning(request, '<p>La carte a été refusée, veuillez réessayer.</p>')

			else: # Si le formulaire n'est pas valide.
				form = OrderCreateForm(request.POST) #On recharge la page avec les données renseignées en montrant l'erreur.
				return render(request, "commandes/orders-create.html", {'cart':cart, 'final_composed_cart':final_composed_cart, 'form':form})
		else:
			form = OrderCreateForm()
			return render(request, "commandes/orders-create.html", {'cart':cart, 'final_composed_cart':final_composed_cart, 'form':form})
	
	else:
		form = OrderCreateForm()
		return render(request, "commandes/orders-create.html", {'cart':cart, 'final_composed_cart':final_composed_cart, 'form':form})

def order_created(request):
	return render(request, "commandes/orders-create.html", {})

