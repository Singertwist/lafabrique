from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse, HttpResponseForbidden
from .actions import export_as_csv_action, export_to_csv

# Register your models here.

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	# raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['order_number', 'picking_date', 'prenom', 'nom', 'paid', 'created', 'updated', 'closed_order']
	list_filter = ['paid', 'created', 'updated']
	inlines = [OrderItemInline]
	actions = [export_as_csv_action("CSV Export"), export_to_csv]


class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['order', 'type_product', 'obtenir_articles', 'price', 'quantity']
	actions = [export_as_csv_action("CSV Export"), export_to_csv]


	def obtenir_articles(self, obj):
		return ",".join([p.nom_article_variation for p in obj.product.all()])
	obtenir_articles.short_description = 'Articles commandés' #Renommer l'entête de colonne
	obtenir_articles.allow_tags = True 



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

