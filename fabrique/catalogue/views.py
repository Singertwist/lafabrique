from django.shortcuts import render, get_object_or_404
from catalogue.models import Categories_Article, Sous_Categories_Article, Article
from django.db.models import Q # Permet de réaliser des requêtes complexes avec OR/OU par exemple

# Create your views here.
#def articles_plats(request, slug, ordre):
#	sous_categories_articles = get_object_or_404(Categories_Article, slug=slug, ordre=ordre)
#	sous_categories_articles = sous_categories_articles.sous_categories_article_set.all()
#	return render(request, "commander.html", {'sous_categories_articles':sous_categories_articles})

def articles_plats(request, slug, ordre):
	categories_articles = get_object_or_404(Categories_Article, slug=slug, ordre=ordre)
	sous_categories_articles = categories_articles.sous_categories_article_set.all()
	if sous_categories_articles.filter(plats=True).exists() == False:
		sous_categories_articles = Article.objects.filter(categories__categorie__id = ordre)
	else:
		sous_categories_articles
	return render(request, "commander.html", {'sous_categories_articles':sous_categories_articles})


#def articles_desserts(request, id=None, categories_articles=None, slug=None):
#	return render(request,"commander-dessert.html", {})