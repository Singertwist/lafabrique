from django.conf import settings
from catalogue.models import Categories_Article, Sous_Categories_Article, Article

#Fonction permettant d'afficher dans base-commander.html les données relatives aux catégories du menu commander.
def menu_commander(request):
    menu_commander_categories = Categories_Article.objects.filter(actif=1).order_by('ordre')
    return {'menu_commander_categories': menu_commander_categories}