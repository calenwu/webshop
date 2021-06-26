from django import forms
from django.utils.translation import gettext_lazy as _
from shop.models import ProductCategory


class FilterForm(forms.Form):
	search = forms.CharField(
		label=_('Search'), 
		max_length=255,
		required=False,
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Search'),
			}
		)
	)
	category = forms.ModelChoiceField(
		label=_('Category'),
		required=False,
		widget=forms.Select(),
		queryset=ProductCategory.objects.all(),
		to_field_name='slug',
		empty_label=_('Show all')
	)
