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
# from django.conf.urls import url Ancienne codification URL Django 1.11
from django.contrib import admin
from . import views

urlpatterns = [
	path('connexion/', views.checkout_account, name='checkout_account'),
	path('resume/', views.order_create, name='order_create'),
	path('admin/order/<int:order_id>/',	views.admin_order_detail, name='admin_order_detail'),
]

# urlpatterns = [
# 	url(r'connexion/$', views.checkout_account, name='checkout_account'),
# 	url(r'resume/$', views.orders_create, name='orders_create'),
# ]
