from django import forms
from datetime import datetime, timedelta
from django.utils import timezone

#PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
def one_hour_from_now():
	test = datetime.now() + timedelta(hours=1)
	return test.strftime("%Y-%m-%d %H:%M:%S")
# picking_date = forms.DateTimeField(initial=one_hour_from_now, label='Date et heure de retrait de la commande:')

class CartAddProductForm(forms.Form):
	quantity = forms.IntegerField(min_value=1, max_value=1, initial=1, widget=forms.HiddenInput)
	next =  forms.CharField(widget=forms.HiddenInput, max_length=2000)
	#update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
	#quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)

class ComposedCartAddProductForm(forms.Form):
	quantity = forms.IntegerField(min_value=1, max_value=1, initial=1, widget=forms.HiddenInput)
	comment = forms.CharField(label="Un petit commentaire à ajouter?", required=False, widget=forms.Textarea(attrs={'placeholder': 'Un petit quelque chose à nous dire ? - Max 150 caractères', 'maxlength':'150'}))
	next =  forms.CharField(widget=forms.HiddenInput, max_length=2000)

class DatePickerForm(forms.Form):
	picking_date = forms.DateTimeField(label='Date et heure de retrait de la commande:')

	def clean_picking_date(self):
		date = self.cleaned_data["picking_date"]
		if date <= timezone.now():
			raise forms.ValidationError('Veuillez ne pas saisir une date antérieure à ce jour.')
		if date > timezone.now() + timedelta(weeks=2):
			raise forms.ValidationError('Oula, vous voyez loin ! Veuillez saisir une date inférieure à 2 semaines.')
		return date