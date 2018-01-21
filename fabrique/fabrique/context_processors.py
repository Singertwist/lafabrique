from django.conf import settings
from django.db.models import Q 
from catalogue.models import Categories_Article, Sous_Categories_Article, Article
from producteurs.models import Categories, Producteurs, Equipes
from panier.cart import Cart

#Fonction permettant d'afficher dans base-commander.html les données relatives aux catégories du menu commander.
def menu_commander(request):
    menu_commander_categories = Categories_Article.objects.filter(actif=1).order_by('ordre')
    return {'menu_commander_categories': menu_commander_categories}

def menu_producteurs(request):
	menu_producteurs_categories = Categories.objects.filter(actif=1, categorie_principale=1).order_by('ordre')
	return {'menu_producteurs_categories': menu_producteurs_categories}

def panier(request):
	cart = Cart(request)
	return {'cart':cart}