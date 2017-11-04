#-*- coding: utf-8 -*-
from django.shortcuts import render
from catalogue.models import Categories_Article, Sous_Categories_Article, Article


def home(request):
	return render(request, "index.html", {})