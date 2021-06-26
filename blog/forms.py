from django import forms
from django.utils.translation import gettext_lazy as _


class ArticlesFilterForm(forms.Form):
	search = forms.CharField(
		label=_('Search'),
		widget=forms.TextInput(attrs={'type': 'text', 'placeholder': _('Search')})
	)
