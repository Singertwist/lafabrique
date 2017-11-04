from django.contrib import admin

# Register your models here.
from django.utils.text import Truncator
from .models import Categories_Article, Sous_Categories_Article, Article

class Categories_ArticleAdmin(admin.ModelAdmin):
  list_display   = ('nom', 'timestamp', 'updated', 'ordre', 'actif')
  list_filter    = ('nom', )
  ordering       = ('ordre', )
  search_fields  = ('nom', )
  prepopulated_fields = {'slug': ('nom', ), } 

class Sous_Categories_ArticleAdmin(admin.ModelAdmin):
	"""docstring for Categories_articleAdmin"""
	list_display   = ('nom', 'timestamp', 'updated', 'publier')
	list_filter    = ('nom', 'updated', 'publier')
	ordering       = ('nom', 'timestamp')
	search_fields  = ('nom', 'description')
	prepopulated_fields = {'slug': ('nom', ), }

	fieldsets = (
    # Fieldset 1 : meta-info
   ('Configuration de la catégorie', {
        'fields': ('nom', 'slug', 'prix_min', 'image', 'publier', 'categorie', 'plats')
    }),
    # Fieldset 2 : contenu de la catégorie
    ('Description de la catégorie', {
       'description': 'Description de la catégorie des articles. Limiter le nombre de caractères',
       'fields': ('description', )
    }),
)

class ArticleAdmin(admin.ModelAdmin):
	list_display   = ('nom', )
	list_filter    = ('nom','updated', 'disponible')
	ordering       = ('nom', 'timestamp')
	search_fields  = ('nom', 'description')
	prepopulated_fields = {'slug': ('nom', ), }
	
	fieldsets = (
    # Fieldset 1 : meta-info du produits
   ('Configuration générale du produit', {
        'fields': ('nom', 'slug', 'categories', 'image', 'disponible', 'sous_categories_articles')
    }),

    # Fieldset 2 : information nutritive du produits
    ('Informations nutritives produits', {
       'fields': ('allergenes', 'gluten_info', 'vegeterien_info', 'ingredients', 'producteurs')
    }),

    # Fieldset 3 : information nutritive du produits
    ('Description du produit', {
       'fields': ('description_produit', )
    }),

    # Fieldset 4 : information financière du produit
    ('Informations financières du produit', {
       'fields': ('unite_produit', 'prix_unitaire', 'taux_TVA')
    }),
)

admin.site.register(Categories_Article, Categories_ArticleAdmin)
admin.site.register(Sous_Categories_Article, Sous_Categories_ArticleAdmin)
admin.site.register(Article, ArticleAdmin)
