from rest_framework import serializers
from catalogue.models import Variations_Articles, Article, Sous_Categories_Article, Categories_Article

class SousCategoriesArticlesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sous_Categories_Article
		fields = '__all__'

class ArticlesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = '__all__'

class VariationsArticlesSerializer(serializers.ModelSerializer):
	article = ArticlesSerializer()
	categories = SousCategoriesArticlesSerializer()
	class Meta:
		model = Variations_Articles
		fields = '__all__'
