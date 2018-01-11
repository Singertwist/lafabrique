from django.shortcuts import render
from django.utils.crypto import get_random_string
# Create your views here.

#def panier_id(request):
#	if request.session.get('id_panier') is None:
#		request.session['id_panier'] = get_random_string(length=50)
#		return request.session['id_panier']
#	else:
#		request.session.get('id_panier')
#		return request.session['id_panier']

def panier(request):
	return render(request, "panier/panier.html", {})