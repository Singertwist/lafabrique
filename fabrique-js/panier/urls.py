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

#from django.conf.urls import url #Ancienne méthode de codification des URL.
from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
	path('panier/', views.cart_detail, name='cart_detail'),
    path('cart-add-quantity-final-composed-cart/<str:dict_key>/', views.cart_add_quantity_final_composed_cart, name='cart_add_quantity_final_composed_cart'),
	path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove-final-composed-cart/<str:dict_key>/', views.cart_remove_final_composed_cart, name='cart_remove_final_composed_cart'),
	path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('remove-one-final-composed-cart/<str:dict_key>/', views.cart_remove_one_quantity_final_composed_cart, name='cart_remove_one_quantity_final_composed_cart'),
    path('remove-one/<int:product_id>/', views.cart_remove_one, name='cart_remove_one'),
    path('add-composed-cart/<int:categorie_composed_cart>/', views.add_to_final_composed_cart, name='add_to_final_composed_cart'),
    path('remove-composed-cart/<int:categorie_composed_cart>/', views.remove_composed_cart, name='remove_composed_cart'),
    path('cart-modify-final-composed-cart/<int:categorie_composed_cart>-<str:dict_key>/', views.cart_modify_final_composed_cart, name='cart_modify_final_composed_cart'),
    path('cart_existence/', views.cart_existence, name='cart_existence' ),
]

# urlpatterns = [
#     url(r'^panier/', views.cart_detail, name='cart_detail'),
#     url(r'^cart-add-quantity-final-composed-cart/(?P<dict_key>.+)/$', views.cart_add_quantity_final_composed_cart, name='cart_add_quantity_final_composed_cart'),
#     url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
#     url(r'^remove-final-composed-cart/(?P<dict_key>.+)/$', views.cart_remove_final_composed_cart, name='cart_remove_final_composed_cart'),
#     url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
#     url(r'^remove-one-final-composed-cart/(?P<dict_key>.+)/$', views.cart_remove_one_quantity_final_composed_cart, name='cart_remove_one_quantity_final_composed_cart'),
#     url(r'^remove-one/(?P<product_id>\d+)/$', views.cart_remove_one, name='cart_remove_one'),
#     url(r'^add-composed-cart/(?P<categorie_composed_cart>\d+)/$', views.add_to_final_composed_cart, name='add_to_final_composed_cart'),
#     url(r'^remove-composed-cart/(?P<categorie_composed_cart>\d+)/$', views.remove_composed_cart, name='remove_composed_cart'),
#     url(r'^cart-modify-final-composed-cart/(?P<categorie_composed_cart>\d+)-(?P<dict_key>.+)/$', views.cart_modify_final_composed_cart, name='cart_modify_final_composed_cart'),
# ]
