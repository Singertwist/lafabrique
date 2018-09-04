from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	# raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['order_number', 'picking_date', 'prenom', 'nom', 'paid', 'created', 'updated', 'closed_order']
	list_filter = ['paid', 'created', 'updated']
	inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

