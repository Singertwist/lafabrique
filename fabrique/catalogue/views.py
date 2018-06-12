from django.shortcuts import render, get_object_or_404
from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit
from panier.forms import CartAddProductForm, ComposedCartAddProductForm
from django.db.models import Q # Permet de réaliser des requêtes complexes avec OR/OU par exemple
from django.utils.crypto import get_random_string
from panier.cart  import Cart, ComposedCart
# Create your views here.
def articles_plats(request, slug, ordre):
	categories_articles = get_object_or_404(Categories_Article, slug=slug, ordre=ordre, actif=1) # On récupérer la catégorie sur laquelle on clique (plats, desserts, boissons). L'ordre permet d'ordonner le menu, par exemple si Boissons --> 1 alors, la catégorie boisson apparaitra en premier.
	sous_categories_articles = categories_articles.sous_categories_article_set.filter(publier=1) # Une fois la catégorie sélectionner, on s'intéresse à toutes les sous catégories relatives à la catégorie principale. Par exemple, pour la catégorie plat, il y aura plusieurs sous-catégories (sandwiches, soupes,...) alors que pour la catégorie Boissons --> Il n'y aura qu'une sous-catégorie -->Boissons.
	if sous_categories_articles.filter(plats=True).exists() == False: # Si dans la / les sous catégories, il y a une sous-catégorie dont le champ "Est un plat" est coché (.exists() permet de s'assurer que la Queryset est vide ou non). Si la QUeryset est vide alors, cela veut dire qu'il faut que l'on affiche directement les sous catégories.
		sous_categories_articles = Article.objects.filter(categories__categorie_id=categories_articles.id, disponible=1) # On filtre sur tous les articles ayant le même ID en catégories que la catégories principales.
	else:
		sous_categories_articles # S'il s'agit d'une sous catégorie, alors on reprend toutes les sous catégories qui ont été sélectionnées.

	cart_product_form = CartAddProductForm()

	return render(request, "catalogue/commander.html", {'sous_categories_articles':sous_categories_articles, 'categories_articles':categories_articles, 'cart_product_form': cart_product_form})

def articles_plats_composer(request, id, slug):
	sous_categories_articles = get_object_or_404(Sous_Categories_Article, id=id, slug=slug) #On récupére les sous-catégories d'articles (sandwiches, soupe,...)
	articles = sous_categories_articles.article_set.filter(disponible=1, article_composer=1) #Pour chacune de ces sous catégories, on isole tous les articles concernés disponibles et pouvant servir à composer une recette
	id_type_produit_article = articles.values('sous_categories_articles_id') #Pour chaque article, celui-ci dispose d'un attribut type de produit (pain, légume), on récupére l'ID du type de produit.
	type_produit = Type_Produit.objects.filter(id__in=id_type_produit_article) #On ne prend via un filtre que les Types de produits (model) qui sont présent dans les articles
	
	cart_product_form = CartAddProductForm() # Nécessaire si on veut ajouter des articles provenant de plats non composés.
	composed_cart_product_form = ComposedCartAddProductForm()
	composed_cart = ComposedCart(request)
	return render(request, "catalogue/commander-suite-composer.html",{'sous_categories_articles':sous_categories_articles, 'type_produit':type_produit, 'articles':articles, 'cart_product_form':cart_product_form, 'composed_cart':composed_cart, 'composed_cart_product_form':composed_cart_product_form})

def articles_plats_pret(request, id, slug):
	sous_categories_articles = get_object_or_404(Sous_Categories_Article, id=id, slug=slug) #On récupère les sous catégories d'articles concernées.
	articles = sous_categories_articles.article_set.filter(disponible=1, article_composer=0) #Pour chacune des sous-catégories, on sélectionne tous les articles disponibles et n'étant pas considéré comme des ingrédients, mais des plats.

	cart_product_form = CartAddProductForm()

	return render(request, "catalogue/commander-suite-pret.html", {'sous_categories_articles':sous_categories_articles, 'articles':articles, 'cart_product_form': cart_product_form})
