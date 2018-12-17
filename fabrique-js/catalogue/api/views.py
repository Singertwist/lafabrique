from rest_framework.generics import ListAPIView, RetrieveAPIView
from catalogue.models import Categories_Article, Sous_Categories_Article, Allergie, Unite_Oeuvre, Type_Produit, Type_Variations_Articles, Taux_TVA, Article, Variations_Articles
from django.shortcuts import render, get_object_or_404


from .serializers import VariationsArticlesSerializer, SousCategoriesArticlesSerializer

class VariationsArticlesAllList(ListAPIView):
	serializer_class = VariationsArticlesSerializer
	queryset =  Variations_Articles.objects.all()

class SousCategoriesArticlesList(ListAPIView):
	serializer_class = SousCategoriesArticlesSerializer
	queryset =  Sous_Categories_Article.objects.all()

class SousCategoriesArticlesDetail(RetrieveAPIView):
	serializer_class = SousCategoriesArticlesSerializer
	queryset =  Sous_Categories_Article.objects.all()

class ArticlesUneList(ListAPIView):
	serializer_class = VariationsArticlesSerializer

	def get_queryset(self):
		articles_une = Variations_Articles.objects.filter(article_une=1)

		return articles_une

class ArticleDetail(RetrieveAPIView):
	serializer_class = VariationsArticlesSerializer
	queryset =  Variations_Articles.objects.all()

class VariationsArticlesList(ListAPIView):

	def get_queryset(self):
		categories_articles = get_object_or_404(Categories_Article, slug=self.kwargs['slug'], ordre=self.kwargs['ordre'], actif=1)
		sous_categories_articles = categories_articles.sous_categories_article_set.filter(publier=1)

		if sous_categories_articles.filter(plats=True).exists() == False:
			sous_categories_articles = Variations_Articles.objects.filter(categories__categorie_id=categories_articles.id, variation_disponible=1, article__disponible=1)
			return sous_categories_articles
		else:
			return sous_categories_articles


# Nécessaire d'utiliser get_serializer_class car sous_categories_articles peut être sous une queryset contenant ls variations articles soit une sous catégories d'articles. Ce qui veut dire que cela peut être le serializers 
# SousCategoriesArticlesSerializer ou VariationsArticlesSerializer
	def get_serializer_class(self):
		categories_articles = get_object_or_404(Categories_Article, slug=self.kwargs['slug'], ordre=self.kwargs['ordre'], actif=1)
		sous_categories_articles = categories_articles.sous_categories_article_set.filter(publier=1)

		if sous_categories_articles.filter(plats=True).exists() == False:
			return VariationsArticlesSerializer
		else:
			return SousCategoriesArticlesSerializer
