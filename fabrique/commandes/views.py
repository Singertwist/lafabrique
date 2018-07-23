from django.shortcuts import render
from panier.cart  import Cart, ComposedCart, FinalComposedCart

# Create your views here.

def checkout_account(request):
	return render(request, "commandes/checkout-account.html", {})

def orders_create(request):
	if bool(request.session.get('final_composed_cart')) or bool(request.session.get('cart')): #Condition nécessaire pour affciher si les deux paniers, final_composed_cart et cart sont vides.
		final_composed_cart = FinalComposedCart(request)
		cart = Cart(request)
	else:
		final_composed_cart = None
		cart = None
	return render(request, "commandes/orders-create.html", {'cart':cart, 'final_composed_cart':final_composed_cart})