from django import forms
from django.core.validators import RegexValidator
from .models import Order

class OrderCreateForm(forms.ModelForm):
	card_holder_name = forms.CharField(max_length=255, label='Nom du possesseur de la carte :')
	card_number = forms.IntegerField(min_value=0, label='Numéro de carte :') #Nombre minimum de digit sur une carte 13 et nombre max 16.
	card_validity_date = forms.CharField(max_length=5, label ='Date de validité :', validators=[RegexValidator('(0[1-9]|1[0-2])\/[0-9]{2}', message="Veuillez saisir une date d'expiration valide au format MM/AA")])
	cvv_number = forms.IntegerField(min_value=99, max_value=1000, label='Code Secret (CVV) :')
	stripe_id = forms.CharField(widget=forms.HiddenInput())
	class Meta:
		model = Order
		fields = ['prenom', 'nom', 'adresse', 'code_postal', 'ville', 'email', 'card_holder_name', 'card_number', 'card_validity_date', 'cvv_number', 'stripe_id']
		widgets = {
			'prenom': forms.TextInput(attrs={'placeholder': 'Votre Prénom - Ex: Claude'}),
			'nom': forms.TextInput(attrs={'placeholder': 'Votre Nom - Ex: Dupont'}),
			'adresse': forms.TextInput(attrs={'placeholder': 'Votre Adresse - Ex: 10 Rue du Calvaire'}),
			'code_postal': forms.TextInput(attrs={'placeholder': 'Votre Code Postal - Ex: 10000'}),
			'ville': forms.TextInput(attrs={'placeholder': 'Votre Ville - Ex: Troyes'}),
			'email': forms.EmailInput(attrs={'placeholder': 'Votre Adresse Email - Ex: claude.dupont@troyes.fr'}),
			}