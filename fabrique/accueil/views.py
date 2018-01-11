#-*- coding: utf-8 -*-
from django.shortcuts import render
from catalogue.models import Categories_Article, Sous_Categories_Article, Article
from django.utils.crypto import get_random_string

def home(request):
	if request.session.get('id_panier') is None:
		request.session['id_panier'] = get_random_string(length=50)
		id_panier = request.session['id_panier']
	else:
		request.session.get('id_panier')
		id_panier = request.session['id_panier']
	return render(request, "accueil/index.html", {})

def contact(request):
	if request.session.get('id_panier') is None:
		request.session['id_panier'] = get_random_string(length=50)
		id_panier = request.session['id_panier']
	else:
		request.session.get('id_panier')
		id_panier = request.session['id_panier']
	return render(request, "accueil/contact.html", {'id_panier':id_panier})