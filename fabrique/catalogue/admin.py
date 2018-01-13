from django.contrib import admin

# Register your models here.
from django.utils.text import Truncator
from .models import Categories_Article, Sous_Categories_Article, Article, Allergie, Unite_Produit, Type_Produit

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
        'fields': ('nom', 'slug', 'prix_min', 'image', 'publier', 'categorie', 'plats', 'composer')
    }),
    # Fieldset 2 : contenu de la catégorie
    ('Description de la catégorie', {
       'description': 'Description de la catégorie des articles. Limiter le nombre de caractères',
       'fields': ('description', )
    }),
)

class ArticleAdmin(admin.ModelAdmin):
  list_display   = ('nom', 'prix_unitaire', 'disponible')
  list_filter    = ('nom','updated', 'disponible')
  ordering       = ('nom', 'timestamp')
  search_fields  = ('nom', 'description')
  list_editable = ('prix_unitaire', 'disponible')
  prepopulated_fields = {'slug': ('nom', ), }

  fieldsets = (
    # Fieldset 1 : meta-info du produits
   ('Configuration générale du produit', {
        'fields': ('nom', 'slug', 'categories', 'image', 'disponible', 'article_composer', 'sous_categories_articles')
    }),

    # Fieldset 2 : information nutritive du produits
    ('Informations nutritives produits', {
       'fields': ('allergenes', 'gluten_info', 'vegeterien_info', 'type_plat_info', 'ingredients', 'producteurs')
    }),

    # Fieldset 3 : information nutritive du produits
    ('Description du produit', {
       'fields': ('description', )
    }),

    # Fieldset 4 : information financière du produit
    ('Informations financières du produit', {
       'fields': ('unite_produit', 'prix_unitaire', 'taux_TVA')
    }),
)

class AllergieAdmin(admin.ModelAdmin):
  list_display   = ('nom', 'timestamp', 'updated', 'active')
  list_filter    = ('nom', )
  ordering       = ('nom', )
  search_fields  = ('nom', )
  prepopulated_fields = {'slug': ('nom', ), } 

class Unite_ProduitAdmin(admin.ModelAdmin):
  list_display   = ('nom', 'timestamp', 'updated', 'active')
  list_filter    = ('nom', )
  ordering       = ('nom', )
  search_fields  = ('nom', )
  prepopulated_fields = {'slug': ('nom', ), }

class Type_ProduitAdmin(admin.ModelAdmin):
  list_display   = ('nom', 'timestamp', 'updated', 'active')
  list_filter    = ('nom', )
  ordering       = ('nom', )
  search_fields  = ('nom', )
  prepopulated_fields = {'slug': ('nom', ), }



admin.site.register(Categories_Article, Categories_ArticleAdmin)
admin.site.register(Sous_Categories_Article, Sous_Categories_ArticleAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Allergie, AllergieAdmin)
admin.site.register(Unite_Produit, Unite_ProduitAdmin)
admin.site.register(Type_Produit, Type_ProduitAdmin)
