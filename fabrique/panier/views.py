from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit, Variations_Articles
from panier.cart  import Cart, ComposedCart, FinalComposedCart, CartDataValidation
from panier.forms import CartAddProductForm, ComposedCartAddProductForm, DatePickerForm
from django.contrib import messages
# Create your views here.

@require_POST
def cart_add(request, product_id):
	product = get_object_or_404(Variations_Articles, id=product_id)
	cart = Cart(request)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		next = cd['next'] # Permet d'enregistrer la page précédente et d'y retourner une fois la quantité ajoutée dans le panier.
		var = cart.add(product=product, quantity=cd['quantity']) # Ajout de la variable var, cette variable permet de récupérer le message de validation afin d'afficher un message.

		if var=="Same_articles":
			messages.warning(request, '<p>Vous ne pouvez pas ajouter deux fois le même article !</p>')
		if var =="Only_one_base":
			messages.warning(request, '<p>OUPS !</p><p> Veuillez n\'ajouter qu\'une seule base à votre composition! </p>')
			
	return HttpResponseRedirect(next) # Redirection vers la page d'où le produit a été ajouté.

def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Variations_Articles, id=product_id)
	cart.remove(product)
	return redirect('cart_detail')

def cart_remove_one(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Variations_Articles, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		next = cd['next'] # Permet d'enregistrer la page précédente et d'y retourner une fois la quantité ajoutée dans le panier.
		cart.remove_one(product=product, quantity=cd['quantity'])
	return HttpResponseRedirect(next) # Redirection vers la page précédente.

def cart_detail(request):
	cart_product_form = CartAddProductForm()
	composed_cart = ComposedCart(request)
	cart_data_validation = CartDataValidation(request)

	if bool(request.session.get('final_composed_cart')) or bool(request.session.get('cart')): #Condition nécessaire pour affciher si les deux paniers, final_composed_cart et cart sont vides.
		final_composed_cart = FinalComposedCart(request)
		cart = Cart(request)
	else:
		final_composed_cart = None
		cart = None

	date_picking_form = DatePickerForm(request.POST or None)
	if date_picking_form.is_valid():
		date = date_picking_form.cleaned_data['picking_date']
		cart_data_validation.add_date(date=date)
		date_picking_form = DatePickerForm()
		return redirect('checkout_account')
	#final_composed_cart = request.session.get('final_composed_cart')

	return render(request, 'panier/panier.html', {'cart':cart, 'composed_cart':composed_cart, 'cart_product_form':cart_product_form, 'final_composed_cart':final_composed_cart, 'date_picking_form':date_picking_form, 'cart_data_validation':cart_data_validation})

#Création d'un plat personnalisé

def add_to_final_composed_cart(request, categorie_composed_cart):
	categorie_composed_cart = get_object_or_404(Sous_Categories_Article, id=categorie_composed_cart)
	final_composed_cart = FinalComposedCart(request)
	form = ComposedCartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		next = cd['next']
		if request.session.get('final_composed_cart') != None: # Condition nécessaire lorsque le panier composé n'est pas encore initialié (aucun article ajouté) et que l'on essaye d'ajouter un panier composé vide au panier final. Retour None et une erreur. Pour éviter cela, on vérifie si le panier est retourne une valeur None.
			var = final_composed_cart.add_to_final_composed_cart(categorie_composed_cart=categorie_composed_cart, quantity=cd['quantity'], comment=cd['comment']) # Ajout de la variable var, cette variable permet de récupérer le message de validation afin d'afficher un message.
			if var == "Sucess":
				messages.success(request, '<p>YAHOU !</p><p>Votre composition a bien été ajoutée à votre panier !</p>')
			if var =="Zero_quantity":
				messages.warning(request, '<p>OUPS !</p><p> Veuillez au moins ajouter une base et un accompagnement à votre composition !</p>')
		else:
			messages.warning(request, '<p>OUPS !</p><p> Veuillez au moins ajouter une base et un accompagnement à votre composition !</p>')
			return HttpResponseRedirect(next)
	return HttpResponseRedirect(next)

def remove_composed_cart(request, categorie_composed_cart):
	categorie_composed_cart = get_object_or_404(Sous_Categories_Article, id=categorie_composed_cart)
	composed_cart = ComposedCart(request)
	form = ComposedCartAddProductForm(request.POST)
	if form.is_valid():
			cd = form.cleaned_data
			next = cd['next']
			composed_cart.remove_composed_cart(categorie_composed_cart=categorie_composed_cart)
	return HttpResponseRedirect(next)

def cart_remove_final_composed_cart(request, dict_key):
	final_composed_cart = FinalComposedCart(request)
	final_composed_cart.remove_final_composed_cart(dict_key)
	return redirect('cart_detail')

def cart_add_quantity_final_composed_cart(request, dict_key):
	final_composed_cart = FinalComposedCart(request)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		next = cd['next']
		final_composed_cart.add_quantity_final_composed_cart(dict_key=dict_key)
	return redirect(next)

def cart_remove_one_quantity_final_composed_cart(request, dict_key):
	final_composed_cart = FinalComposedCart(request)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		next = cd['next']	
		final_composed_cart.remove_one_quantity_final_composed_cart(dict_key)
	return redirect(next)

def cart_modify_final_composed_cart(request, categorie_composed_cart, dict_key):
	categorie_composed_cart = get_object_or_404(Sous_Categories_Article, id=categorie_composed_cart)
	final_composed_cart = FinalComposedCart(request)
	final_composed_cart.cart_modify_final_composed_cart(dict_key)
	return redirect('articles_plats_composer', slug = categorie_composed_cart.slug , id = categorie_composed_cart.id)



