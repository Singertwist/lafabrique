from django.shortcuts import render, get_object_or_404
from producteurs.models import Categories, Producteurs, Equipes
# Create your views here.


def producteurs(request, slug, ordre):
	categories_producteurs = get_object_or_404(Categories, slug=slug, ordre=ordre)
	if 	categories_producteurs.producteurs_set.all().exists() == False:
		producteurs = categories_producteurs.equipes_set.all()
	else:
		producteurs = categories_producteurs.producteurs_set.all()
	return render(request, "producteurs/producteurs.html",{'categories_producteurs':categories_producteurs,'producteurs':producteurs })