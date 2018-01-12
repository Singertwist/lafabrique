from django import forms

class ArticleAjoutPanierForm(forms.Form):
	quantite = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2','value':'1', 'class':'quantity', 'maxlength':'5'}),^error_messages={'invalid':'Please enter a valid quantity.'}, min_value=1)
	article_id = forms.IntegerField()


