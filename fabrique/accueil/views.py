#-*- coding: utf-8 -*-
from django.shortcuts import render
from catalogue.models import Categories_Article, Sous_Categories_Article, Article
from django.utils.crypto import get_random_string

def home(request):
	return render(request, "accueil/index.html", {})

def contact(request):
	return render(request, "accueil/contact.html", {})