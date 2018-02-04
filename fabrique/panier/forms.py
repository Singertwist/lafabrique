from django import forms

#PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
	quantity = forms.IntegerField(min_value=1, max_value=1, initial=1, widget=forms.HiddenInput)
	next =  forms.CharField(widget=forms.HiddenInput, max_length=2000)
	#update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
	#quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)

class ComposedCartForm(forms.Form):
	quantity = forms.IntegerField(min_value=1, max_value=1, initial=1, widget=forms.HiddenInput)
	next =  forms.CharField(widget=forms.HiddenInput, max_length=2000)