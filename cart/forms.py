from django import forms
from django.utils.translation import gettext_lazy as _

from shop.models import ProductColorQuantity


class AddProductToCartForm(forms.Form):
	size = forms.ModelChoiceField(
		queryset=ProductColorQuantity.objects.all(),
	)
	quantity = forms.CharField()
	update = forms.BooleanField(
		required=False,
		initial=False,
		widget=forms.HiddenInput
	)

	def __init__(self, product_color_id, *args, **kwargs):
		super(AddProductToCartForm, self).__init__(*args, **kwargs)
		product_quantities = ProductColorQuantity.objects.get(product_color_id).excluse(quantity=0)
		self.fields['size'] = forms.ModelChoiceField(
			queryset=product_quantities,
			widget=forms.Select,
			empty_label=_('Sold out') if not product_quantities else None
		)

	def clean_quantity(self):
		quantity = self.cleaned_data.get('quantity')
		if quantity.isdigit() and int(quantity) > 0:
			return quantity
		raise forms.ValidationError(_('Enter a positive quantity'))


class ChangeProductQuantityForm(forms.Form):
	quantity = forms.CharField()
	update = forms.BooleanField(required=False, initial=True, widget=forms.HiddenInput)

	def clean_quantity(self):
		quantity = self.cleaned_data.get('quantity')
		if quantity.isdigit() and int(quantity) > 0:
			return quantity
		raise forms.ValidationError(_('Enter a positive quantity'))
