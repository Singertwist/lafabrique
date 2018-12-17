"""fabrique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
#from django.conf.urls import url Ancienne méthode de codification des URL.
from django.contrib import admin
from .views import VariationsArticlesAllList, VariationsArticlesList, SousCategoriesArticlesList, ArticlesUneList, ArticleDetail, SousCategoriesArticlesDetail

urlpatterns = [
    path('articles/', VariationsArticlesAllList.as_view(), name='articles'), # http://127.0.0.1:8000/commander/api/articles/
    path('articles-une/', ArticlesUneList.as_view(), name='articles-une'), # http://127.0.0.1:8000/commander/api/articles-une/
    path('sous-categories-articles/', SousCategoriesArticlesList.as_view(), name='sous-categories-articles'),
    path('sous-categories-article/<int:pk>', SousCategoriesArticlesDetail.as_view(), name='article'), # http://127.0.0.1:8000/commander/api/sous-categories-articles/1
    path('articles/<slug:slug>-<int:ordre>', VariationsArticlesList.as_view(), name='articles_plats_api'),
    path('article/<int:pk>', ArticleDetail.as_view(), name='article'), # http://127.0.0.1:8000/commander/api/article/1

]


# urlpatterns = [
#     path('composer/(?P<slug>.+)-(?P<id>\d+)$', views.articles_plats_composer, name='articles_plats_composer'),
#     url(r'pret/(?P<slug>.+)-(?P<id>\d+)$', views.articles_plats_pret, name='articles_plats_pret'),
#     url(r'(?P<slug>.+)-(?P<ordre>\d+)$', views.articles_plats, name='articles_plats'),
#     #url(r'desserts/', views.articles_desserts, name='articles_desserts'),
# ]
