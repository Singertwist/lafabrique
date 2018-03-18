from django.contrib import admin

from .models import Categories, Producteurs, Equipes

class CategoriesAdmin(admin.ModelAdmin):
  list_display   = ('categorie_personnes', 'timestamp', 'updated', 'actif', 'ordre')
  ordering       = ('ordre', )
  prepopulated_fields = {'slug': ('categorie_personnes', ), } 

class ProducteursAdmin(admin.ModelAdmin):
	"""docstring for Categories_articleAdmin"""
	list_display   = ('nom', 'prenom', 'actif')
	list_filter    = ('nom', 'prenom', 'code_postal', 'updated', 'actif')
	ordering       = ('categorie_producteurs', 'nom', 'actif')
	search_fields  = ('nom', 'prenom',  'description', 'categorie_producteurs',)
	fieldsets = (
    # Fieldset 1 : meta-info
   ('Configuration du producteur', {
        'fields': ('nom', 'prenom', 'photo', 'categorie_producteurs', 'actif', 'afficher_donnees_privees')
    }),
	# Fieldset 2 : information du producteur
   ('Adresse du producteur', {
       'fields': ('rue', 'ville', 'code_postal', 'pays', 'numero_telephone' )
    }),
    # Fieldset 3 : description du producteur
    ('Description du producteur', {
       'description': 'Description du producteur',
       'fields': ('description', )
    }),
    
)

class EquipesAdmin(admin.ModelAdmin):
	list_display   = ('nom', 'prenom', 'actif')
	list_filter    = ('nom', 'prenom', 'updated', 'actif')
	ordering       = ('nom', 'prenom', 'actif')
	search_fields  = ('nom', 'prenom',  'description')
	fieldsets = (
    # Fieldset 1 : meta-info
   ('Configuration de l\'équipier', {
        'fields': ('nom', 'prenom', 'photo', 'description', 'poste', 'categorie_personnel', 'actif', 'afficher_donnees_privees')
    }),   
)


admin.site.register(Producteurs, ProducteursAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Equipes, EquipesAdmin)