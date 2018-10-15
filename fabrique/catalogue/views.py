from django.shortcuts import render, get_object_or_404
from catalogue.models import Categories_Article, Sous_Categories_Article, Article, Type_Produit, Variations_Articles
from panier.forms import CartAddProductForm, ComposedCartAddProductForm
from django.db.models import Q # Permet de réaliser des requêtes complexes avec OR/OU par exemple
from django.utils.crypto import get_random_string
from panier.cart  import Cart, ComposedCart

# Import pour les Class Based Views

from django.views.generic import ListView

# Fin import pour les Class Based Views

class Liste_Articles_Plats(ListView):
	model = Categories_Article
	context_object_name = "sous_categories_articles"
	template_name = "catalogue/commander.html"

	def get_queryset(self):
		categories_articles = get_object_or_404(Categories_Article, slug=self.kwargs['slug'], ordre=self.kwargs['ordre'], actif=1)
		sous_categories_articles = categories_articles.sous_categories_article_set.filter(publier=1)

		if sous_categories_articles.filter(plats=True).exists() == False:
			sous_categories_articles = Variations_Articles.objects.filter(categories__categorie_id=categories_articles.id, variation_disponible=1, article__disponible=1)
			return sous_categories_articles
		else:
			return sous_categories_articles

	def get_context_data(self, **kwargs):
		context = super(Liste_Articles_Plats, self).get_context_data(**kwargs)
		context['categories_articles'] = get_object_or_404(Categories_Article, slug=self.kwargs['slug'], ordre=self.kwargs['ordre'], actif=1)
		context['article_a_la_une'] = Variations_Articles.objects.filter(article_une=1)
		context['cart_product_form'] = CartAddProductForm()
		return context

class Liste_Articles_Plats_Composes(ListView):
	model = Sous_Categories_Article
	context_object_name = "articles"
	template_name = "catalogue/commander-suite-composer.html"

	def get_queryset(self):
		sous_categories_articles = get_object_or_404(Sous_Categories_Article, id=self.kwargs['id'], slug=self.kwargs['slug']) #On récupére les sous-catégories d'articles (sandwiches, soupe,...)
		articles = sous_categories_articles.variations_articles_set.filter(variation_disponible=1, article__article_composer=1, article__disponible=1).order_by('type_article__nom_type_variation_article') #Pour chacune de ces sous catégories, on isole toutes les variations d'articles concernés disponibles (dans la table variation et aussi au niveau de la fiche articles) et pouvant servir à composer une recette
		return articles

	def get_context_data(self, **kwargs):
		context = super(Liste_Articles_Plats_Composes, self).get_context_data(**kwargs)
		context['cart_product_form'] = CartAddProductForm()
		context['composed_cart_product_form'] = ComposedCartAddProductForm()
		context['composed_cart'] = ComposedCart(self.request)
		context['sous_categories_articles'] = get_object_or_404(Sous_Categories_Article, id=self.kwargs['id'], slug=self.kwargs['slug'])
		return context

class Liste_Articles_Plats_Prets(ListView):
	model = Sous_Categories_Article
	context_object_name = "articles"
	template_name = "catalogue/commander-suite-pret.html"

	def get_queryset(self):
		sous_categories_articles = get_object_or_404(Sous_Categories_Article, id=self.kwargs['id'], slug=self.kwargs['slug']) #On récupére les sous-catégories d'articles (sandwiches, soupe,...)
		articles = sous_categories_articles.variations_articles_set.filter(variation_disponible=1, article__article_composer=0, article__disponible=1) 
		return articles

	def get_context_data(self, **kwargs):
		context = super(Liste_Articles_Plats_Prets, self).get_context_data(**kwargs)
		context['cart_product_form'] = CartAddProductForm()
		context['sous_categories_articles'] = get_object_or_404(Sous_Categories_Article, id=self.kwargs['id'], slug=self.kwargs['slug'])
		return context	

# Sauvegarde des fonctions based-view:
# Create your views here.
# def articles_plats(request, slug, ordre):
# 	categories_articles = get_object_or_404(Categories_Article, slug=slug, ordre=ordre, actif=1) # On récupérer la catégorie sur laquelle on clique (plats, desserts, boissons). L'ordre permet d'ordonner le menu, par exemple si Boissons --> 1 alors, la catégorie boisson apparaitra en premier.
# 	sous_categories_articles = categories_articles.sous_categories_article_set.filter(publier=1) # Une fois la catégorie sélectionner, on s'intéresse à toutes les sous catégories relatives à la catégorie principale. Par exemple, pour la catégorie plat, il y aura plusieurs sous-catégories (sandwiches, soupes,...) alors que pour la catégorie Boissons --> Il n'y aura qu'une sous-catégorie -->Boissons.
# 	if sous_categories_articles.filter(plats=True).exists() == False: # Si dans la / les sous catégories, il y a une sous-catégorie dont le champ "Est un plat" est coché (.exists() permet de s'assurer que la Queryset est vide ou non). Si la QUeryset est vide alors, cela veut dire qu'il faut que l'on affiche directement les sous catégories.
# 		sous_categories_articles = Variations_Articles.objects.filter(categories__categorie_id=categories_articles.id, variation_disponible=1, article__disponible=1) # On filtre sur tous les articles ayant le même ID en catégories que la catégories principales.
# 	else:
# 		sous_categories_articles # S'il s'agit d'une sous catégorie, alors on reprend toutes les sous catégories qui ont été sélectionnées.

# 	cart_product_form = CartAddProductForm()

# 	article_a_la_une = Variations_Articles.objects.filter(article_une=1)

# 	return render(request, "catalogue/commander.html", {'sous_categories_articles':sous_categories_articles, 'categories_articles':categories_articles, 'cart_product_form': cart_product_form, 'article_a_la_une':article_a_la_une})

# def articles_plats_composer(request, id, slug):
# 	sous_categories_articles = get_object_or_404(Sous_Categories_Article, id=id, slug=slug) #On récupére les sous-catégories d'articles (sandwiches, soupe,...)
# 	articles = sous_categories_articles.variations_articles_set.filter(variation_disponible=1, article__article_composer=1, article__disponible=1).order_by('type_article__nom_type_variation_article') #Pour chacune de ces sous catégories, on isole toutes les variations d'articles concernés disponibles (dans la table variation et aussi au niveau de la fiche articles) et pouvant servir à composer une recette

# 	cart_product_form = CartAddProductForm() # Nécessaire si on veut ajouter des articles provenant de plats non composés.
# 	composed_cart_product_form = ComposedCartAddProductForm()
# 	composed_cart = ComposedCart(request)
# 	return render(request, "catalogue/commander-suite-composer.html",{'sous_categories_articles':sous_categories_articles, 'articles':articles, 'cart_product_form':cart_product_form, 'composed_cart':composed_cart, 'composed_cart_product_form':composed_cart_product_form})

# def articles_plats_pret(request, id, slug):
# 	sous_categories_articles = get_object_or_404(Sous_Categories_Article, id=id, slug=slug) #On récupère les sous catégories d'articles concernées.
# 	articles = sous_categories_articles.variations_articles_set.filter(variation_disponible=1, article__article_composer=0, article__disponible=1) #Pour chacune des sous-catégories, on sélectionne toutes la variations d'articles disponibles, puis on remonte à la fiche d'article principal pour sélectionner tous les articles correspondant à des plats prêts et étant disponibles. 

# 	cart_product_form = CartAddProductForm()

# 	return render(request, "catalogue/commander-suite-pret.html", {'sous_categories_articles':sous_categories_articles, 'articles':articles, 'cart_product_form': cart_product_form})
