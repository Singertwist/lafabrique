from django import forms
from django.core.validators import RegexValidator
from .models import Order

class OrderCreateForm(forms.ModelForm):
	card_holder_name = forms.CharField(max_length=255, label='Nom du possesseur de la carte :', widget=forms.TextInput(attrs={'placeholder': 'Nom et Prénom incrits sur la carte - Ex: Dupont Claude'}))
	card_number = forms.CharField(label='Numéro de carte :', widget=forms.TextInput(attrs={'placeholder': 'Le numéro de la carte bancaire - Ex : 4242 4242 4242 4242', 'maxlength': '19' })) #Nombre minimum de digit sur une carte 13 et nombre max 16. En comptant les espaces, 19 caractères.
	card_validity_date = forms.CharField(max_length=5, label ='Date de validité :', validators=[RegexValidator('(0[1-9]|1[0-2])\/[0-9]{2}', message="Veuillez saisir une date d'expiration valide au format MM/AA")], widget=forms.TextInput(attrs={'placeholder': 'Date de validité au format MM/AA', 'maxlength': '5'}))
	cvv_number = forms.IntegerField(min_value=100, max_value=9999, label='Code Secret (CVV) :', widget=forms.PasswordInput(attrs={'placeholder': 'Le code secret - Ex: 123', 'maxlength': '4'}))
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