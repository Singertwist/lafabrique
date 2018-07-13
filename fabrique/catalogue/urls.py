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
from django.urls import path, include
#from django.conf.urls import url Ancienne méthode de codification des URL.
from django.contrib import admin
from . import views

urlpatterns = [
    path('composer/<str:slug>-<int:id>', views.articles_plats_composer, name='articles_plats_composer'),
    path('pret/<slug:slug>-<int:id>', views.articles_plats_pret, name='articles_plats_pret'),
    path('<slug:slug>-<int:ordre>', views.articles_plats, name='articles_plats'),
    #url(r'desserts/', views.articles_desserts, name='articles_desserts'),
]


# urlpatterns = [
#     path('composer/(?P<slug>.+)-(?P<id>\d+)$', views.articles_plats_composer, name='articles_plats_composer'),
#     url(r'pret/(?P<slug>.+)-(?P<id>\d+)$', views.articles_plats_pret, name='articles_plats_pret'),
#     url(r'(?P<slug>.+)-(?P<ordre>\d+)$', views.articles_plats, name='articles_plats'),
#     #url(r'desserts/', views.articles_desserts, name='articles_desserts'),
# ]
