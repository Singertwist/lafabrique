#-*- coding: utf-8 -*-
from django.shortcuts import render
from catalogue.models import Categories_Article, Sous_Categories_Article, Article


def home(request):
	request.session.set_test_cookie()
	return render(request, "accueil/index.html", {})

def contact(request):
	if request.session.test_cookie_worked():
		print (">>>>>> Les cookies fonctionnent")
		request.session.delete_test_cookie()
	return render(request, "accueil/contact.html", {})