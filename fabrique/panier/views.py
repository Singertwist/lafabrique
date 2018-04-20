from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit
from panier.cart  import Cart, ComposedCart, FinalComposedCart
from panier.forms import CartAddProductForm
# Create your views here.

#def panier_id(request):
#	if request.session.get('id_panier') is None:
#		request.session['id_panier'] = get_random_string(length=50)
#		return request.session['id_panier']
#	else:
#		request.session.get('id_panier')
#		return request.session['id_panier']

#def panier(request):
#	return render(request, "panier/panier.html", {})

@require_POST
def cart_add(request, product_id):
	product = get_object_or_404(Article, id=product_id)
	cart = Cart(request)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		next = cd['next'] # Permet d'enregistrer la page précédente et d'y retourner une fois la quantité ajoutée dans le panier.
		cart.add(product=product, quantity=cd['quantity'])
	return HttpResponseRedirect(next) # Redirection vers la page d'où le produit a été ajouté.

def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Article, id=product_id)
	cart.remove(product)
	return redirect('cart_detail')

def cart_remove_one(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Article, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		next = cd['next'] # Permet d'enregistrer la page précédente et d'y retourner une fois la quantité ajoutée dans le panier.
		cart.remove_one(product=product, quantity=cd['quantity'])
	return HttpResponseRedirect(next) # Redirection vers la page précédente.

def cart_detail(request):
	cart_product_form = CartAddProductForm()
	cart = Cart(request)
	composed_cart = ComposedCart(request)
	#final_composed_cart = request.session.get('final_composed_cart')
	final_composed_cart = FinalComposedCart(request)
	return render(request, 'panier/panier.html', {'cart':cart, 'composed_cart':composed_cart, 'cart_product_form':cart_product_form, 'final_composed_cart':final_composed_cart})

#Création d'un plat personnalisé

def add_to_final_composed_cart(request, categorie_composed_cart):
	categorie_composed_cart = get_object_or_404(Sous_Categories_Article, id=categorie_composed_cart)
	final_composed_cart = FinalComposedCart(request)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		next = cd['next']
		final_composed_cart.add_to_final_composed_cart(categorie_composed_cart=categorie_composed_cart, quantity=cd['quantity'])
	return HttpResponseRedirect(next)
