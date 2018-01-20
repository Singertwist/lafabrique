from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.crypto import get_random_string
from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit
from panier.cart  import Cart
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
	cart = Cart(request)
	product = get_object_or_404(Article, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])

	return redirect('cart_detail')


def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Article, id=product_id)
	cart.remove(product)
	return redirect('cart_detail')

def cart_detail(request):
	cart = Cart(request)
	cart_product_form = CartAddProductForm()
	return render(request, 'panier/detail.html', locals())