from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse, HttpResponseForbidden
from .actions import export_to_csv, export_to_csv_sales
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	# raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['order_number', 'picking_date', 'prenom', 'nom', 'paid', 'created', 'updated', 'closed_order', 'order_detail']
	list_filter = ['paid', 'created', 'updated']
	inlines = [OrderItemInline]
	actions = [export_to_csv]
	search_fields = ['order_number', 'picking_date', 'prenom', 'nom', 'paid', 'created', 'updated', 'closed_order']
	date_hierarchy = 'created'

	def order_detail(self, obj):
		return mark_safe('<a href="{}">Voir le détail</a>'.format(reverse('admin_order_detail', args=[obj.id])))
	order_detail.short_description = 'Consulter le détail'


class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['order', 'type_product', 'obtenir_articles', 'price', 'quantity']
	actions = [export_to_csv_sales]
	search_fields = ['order__order_number', 'type_product__nom', 'price', 'quantity']

	def obtenir_articles(self, obj):
		return ",".join([p.nom_article_variation for p in obj.product.all()])
	obtenir_articles.short_description = 'Articles commandés' #Renommer l'entête de colonne
	obtenir_articles.allow_tags = True 



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

