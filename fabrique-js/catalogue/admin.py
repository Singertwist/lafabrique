from django.contrib import admin

# Register your models here.
from django.utils.text import Truncator
from .models import Categories_Article, Sous_Categories_Article, Article, Allergie, Unite_Oeuvre, Type_Produit, Taux_TVA, Variations_Articles, Type_Variations_Articles
from commandes.actions import export_to_csv

class Categories_ArticleAdmin(admin.ModelAdmin):
  list_display   = ('nom', 'timestamp', 'updated', 'ordre', 'actif', 'rubrique_principale')
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

class VariationsArticlesInline(admin.TabularInline):
  model = Variations_Articles


class ArticleAdmin(admin.ModelAdmin):
  list_display   = ('nom', 'disponible', 'sous_categories_articles')
  list_filter    = ('nom','updated', 'disponible')
  ordering       = ('nom', 'timestamp')
  search_fields  = ('nom', 'description')
  list_editable = ('disponible', )
  prepopulated_fields = {'slug': ('nom', ), }

  fieldsets = (
    # Fieldset 1 : meta-info du produits
   ('Configuration générale du produit', {
        'fields': ('nom', 'slug', 'image', 'disponible', 'article_composer', 'sous_categories_articles' )
    }),

    # Fieldset 2 : information nutritive du produits
    ('Informations nutritives produits', {
       'fields': ('allergenes', 'gluten_info', 'vegeterien_info', 'type_plat_info', 'ingredients', )
    }),

    # Fieldset 3 : information nutritive du produits
    ('Description du produit', {
       'fields': ('description', )
    }),
)

  inlines = [
        VariationsArticlesInline,
    ]

  actions = [export_to_csv]
  #Défini une fonction afin d'afficher la catégorie de l'article dans la page Afmin, (list_display), car impossible de le faire sur une relation ManyToMany
  # def obtenir_categories(self, obj):
  #   return "<br/>".join([p.nom for p in obj.categories.all()])
  
  # obtenir_categories.short_description = 'Catégories de l\'article' #Renommer l'entête de colonne
  # obtenir_categories.allow_tags = True #Autoriser les tags HTML et ainsi autoriser les retour à la ligne quand il y a plusieurs catégories (balise <br/>).

class VariationsArticlesAdmin(admin.ModelAdmin):
  list_display = ('article', 'nom_article_variation', 'categories', 'prix_vente_unitaire', 'prix_revient')
  actions = [export_to_csv]

class AllergieAdmin(admin.ModelAdmin):
  list_display   = ('nom', 'timestamp', 'updated', 'active')
  list_filter    = ('nom', )
  ordering       = ('nom', )
  search_fields  = ('nom', )
  prepopulated_fields = {'slug': ('nom', ), } 

class Unite_OeuvreAdmin(admin.ModelAdmin):
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

class Taux_TVAAdmin(admin.ModelAdmin):
  list_display   = ('nom_taux_applicable', 'taux_applicable', 'timestamp', 'updated')
  list_filter    = ('nom_taux_applicable', 'taux_applicable', )
  ordering       = ('taux_applicable', )
  search_fields  = ('nom_taux_applicable', 'taux_applicable' )

class Type_Variations_ArticlesAdmin(admin.ModelAdmin):
  list_display   = ('nom_type_variation_article', 'timestamp', 'updated')
  list_filter    = ('nom_type_variation_article', )
  ordering       = ('nom_type_variation_article', )
  search_fields  = ('nom_type_variation_article', )
  prepopulated_fields = {'slug': ('nom_type_variation_article', ), }



admin.site.register(Categories_Article, Categories_ArticleAdmin)
admin.site.register(Sous_Categories_Article, Sous_Categories_ArticleAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Allergie, AllergieAdmin)
admin.site.register(Unite_Oeuvre, Unite_OeuvreAdmin)
admin.site.register(Type_Produit, Type_ProduitAdmin)
admin.site.register(Taux_TVA, Taux_TVAAdmin)
admin.site.register(Type_Variations_Articles, Type_Variations_ArticlesAdmin)
admin.site.register(Variations_Articles, VariationsArticlesAdmin)