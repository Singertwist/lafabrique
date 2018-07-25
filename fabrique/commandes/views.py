from django.shortcuts import render
from panier.cart  import Cart, ComposedCart, FinalComposedCart
from .models import Order, OrderItem
from .forms import OrderCreateForm

# Create your views here.

def checkout_account(request):
	return render(request, "commandes/checkout-account.html", {})

def order_create(request):
	if bool(request.session.get('final_composed_cart')) or bool(request.session.get('cart')): #Condition nécessaire pour affciher si les deux paniers, final_composed_cart et cart sont vides.
		final_composed_cart = FinalComposedCart(request)
		cart = Cart(request)
	else:
		final_composed_cart = None
		cart = None

	if request.method == 'POST':
		if cart != None or final_composed_cart != None: # Condition nécessaire car renvoi une erreur si le panier est vide et que l'on arrive sur la page. Si panier vide on ne valide pas le formulaire.
			form = OrderCreateForm(request.POST)
			if form.is_valid():
				order = form.save()
				for item in cart:
					OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

			form = OrderCreateForm()
			cart.clear()
			return render(request, "commandes/orders-created.html", {'cart':cart, 'final_composed_cart':final_composed_cart, 'form':form })

		form = OrderCreateForm()
		return render(request, "commandes/orders-create.html", {'cart':cart, 'final_composed_cart':final_composed_cart, 'form':form})
	else:
		form = OrderCreateForm()
		return render(request, "commandes/orders-create.html", {'cart':cart, 'final_composed_cart':final_composed_cart, 'form':form})

def order_created(request):
	return render(request, "commandes/orders-create.html", {})