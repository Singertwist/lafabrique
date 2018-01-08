from django.contrib import admin
from .models import PanierItem
# Register your models here.

class PanierItemAdmin(admin.ModelAdmin):
	list_display   = ('timestamp', 'updated')


admin.site.register(PanierItem, PanierItemAdmin)