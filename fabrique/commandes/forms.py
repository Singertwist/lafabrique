from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['prenom', 'nom', 'adresse', 'code_postal', 'ville', 'email']