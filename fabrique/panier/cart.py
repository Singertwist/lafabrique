from panier.models import PanierItem
from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404

#Définir l'ID du panier. Si vide on attribue un ID, sinon on conserve l'ID existant
def _cart_id(request):
	if request.session.get('id_panier') is None:
		request.session['id_panier'] = get_random_string(length=50)

def get_cart_items(request):
	return PanierItem.objects.filter(cart_id=_cart_id(request))

def add_to_cart(request):
	#On copie la requête de type POST dans la variable postdata.
	postdata = request.POST.copy()
	#On cherche à isoler l'ID unique du produit qui vient d'être ajouté au produit
	article_id = postdata.get('article_id','')
	#On ajoute la quantite, par défaut, quantité de 1
	quantite = postdata.get('quantite',1)
	#On va chercher l'article concerné dans la base de données
	article = get_object_or_404(Article, id=article_id)
	#On veut ajouter l'article dans le panier
	panier_articles = get_cart_items(request)
	#Mais avant on vérifie que le produit n'est pas déjà dans le panier.
	#produit_dans_panier = False

	pi = PanierItem()
	pi.article = article
	pi.quantite = quantite
	pi.panier_id = _cart_id(request)
	pi.save()
