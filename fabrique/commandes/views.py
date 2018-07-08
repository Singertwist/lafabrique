from django.shortcuts import render

# Create your views here.

def checkout_account(request):
	return render(request, "commandes/checkout-account.html", {})

def orders_create(request):
	return render(request, "commandes/orders-create.html", {})