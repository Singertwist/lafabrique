from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse, HttpResponseForbidden
from .actions import export_as_csv_action


import csv
import datetime

def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; \filename={}.csv'.format(opts.verbose_name)
	writer = csv.writer(response)
	# fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	fields = []
	for field in opts.get_fields():
		if field.many_to_many or field.one_to_many:
			fields.append(field)
		else:
			fields.append(field)

	# Write a first row with header information
	writer.writerow([field.verbose_name for field in fields])

	# Write data rows
	for obj in queryset:
		data_row = []
		for field in fields:
			value = getattr(obj, field.name)
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value)
		writer.writerow(data_row)
	return response
export_to_csv.short_description = 'Export to CSV'


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

