from django import forms
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from account.models import User
from order.models import Country, State, Order, Address, ShippingMethod

import logging

logger = logging.getLogger('django')

class OrderCreateForm(forms.ModelForm):
	email = forms.EmailField(
		label=_('Email'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('example@gmail.com'),
			}
		)
	)
	first_name = forms.CharField(
		label=_('First name'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Luke'),
			}
		)
	)
	last_name = forms.CharField(
		label=_('Last name'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Skywalker'),
			}
		)
	)
	company = forms.CharField(
		label=_('Company (optional)'),
		required=False,
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Company (optional)'),
			}
		)
	)
	address = forms.CharField(
		label=_('Street and house number'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Street and house number'),
			}
		)
	)
	address2 = forms.CharField(
		label=_('Additional address (optional)'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Additional address (optional)'),
			}
		),
		required=False,
	)
	city = forms.CharField(
		label=_('City'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('City'),
			}
		)
	)
	country = forms.CharField(
		label=_('Country'),
		widget=forms.Select(
			attrs={
				'placeholder': _('Country'),
			}
		)
	)
	state = forms.CharField(
		label=_('State'),
		widget=forms.Select(
			attrs={
				'placeholder': _('State'),
				'hidden': True
			}
		),
		required=False
	)
	postal_code = forms.CharField(
		label=_('Postal code'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Postal code'),
			}
		)
	)
	telephone = forms.CharField(
		label=_('Phone'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Phone'),
			}
		)
	)
	newsletter = forms.BooleanField(
		required=False,
		label=_('Keep me up to date on news and exclusive offers'),
	)
	comment = forms.CharField(
		required=False,
		label=_('Comment (optional)'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Comment'),
			}
		)
	)

	class Meta:
		model = Order
		fields = [
			'first_name', 'last_name', 'email', 
			'company', 'address', 'address2', 
			'city', 'country', 'state', 
			'postal_code',  'telephone', 'comment', 'newsletter'
		]

	def __init__(self, *args, **kwargs):
		super(OrderCreateForm, self).__init__(*args, **kwargs)
		self.fields['country'].choices = Country.get_active()
		self.fields['state'].choices = State.get_active()

	def clean(self):
		cleaned_data = super().clean()

	def clean_state(self):
		country = Country.objects.get(iso_2=self.cleaned_data.get('country'))
		state = self.cleaned_data.get('state')
		if not state and len(country.states.all()):
			raise forms.ValidationError(_('Please select a state'))
		if country.states:
			return state
		else:
			return None


class AddressForm(forms.ModelForm):
	user = forms.ModelChoiceField(queryset=QuerySet())
	email = forms.EmailField(
		label=_('Email'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('example@gmail.com'),
			}
		)
	)
	first_name = forms.CharField(
		label=_('First name'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Luke'),
			}
		)
	)
	last_name = forms.CharField(
		label=_('Last name'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Skywalker'),
			}
		)
	)
	company = forms.CharField(
		label=_('Company (optional)'),
		required=False,
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Company (optional)'),
			}
		)
	)
	address = forms.CharField(
		label=_('Street and house number'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Street and house number'),
			}
		)
	)
	address2 = forms.CharField(
		label=_('Additional address (optional)'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Additional address (optional)'),
			}
		),
		required=False,
	)
	city = forms.CharField(
		label=_('City'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('City'),
			}
		)
	)
	country = forms.CharField(
		label=_('Country'),
		widget=forms.Select(
			attrs={
				'placeholder': _('Country'),
				'col': '6'
			}
		)
	)
	state = forms.CharField(
		label=_('State'),
		widget=forms.Select(
			attrs={
				'placeholder': _('State'),
				'hidden': True
			}
		),
		required=False
	)
	postal_code = forms.CharField(
		label=_('Postal code'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Postal code'),
			}
		)
	)
	telephone = forms.CharField(
		label=_('Phone'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Phone'),
			}
		)
	)

	class Meta:
		model = Address
		fields = [
			'first_name', 'last_name', 'email', 
			'company', 'address', 'address2', 
			'city', 'country', 'state', 
			'postal_code',  'telephone', 'user'
		]

	def __init__(self, user_id: int, *args, **kwargs):
		super(AddressForm, self).__init__(*args, **kwargs)
		self.fields['country'].choices = Country.get_active()
		self.fields['state'].choices = State.get_active()
		self.fields['user'].queryset = User.objects.filter(id=user_id)

	def clean(self):
		cleaned_data = super().clean()

	def clean_state(self):
		country = Country.objects.get(iso_2=self.cleaned_data.get('country'))
		state = self.cleaned_data.get('state')
		if not state and len(country.states.all()):
			raise forms.ValidationError(_('Please select a state'))
		if country.states:
			return state
		else:
			return None


class ShippingForm(forms.Form):
	method = forms.ModelChoiceField(
		queryset=ShippingMethod.objects.filter(active=True),
	)

	def __init__(self, weight: int, *args, **kwargs):
		super(ShippingForm, self).__init__(*args, **kwargs)
		temp = ShippingMethod.objects.filter(active=True, min_weight__lte=weight, max_weight__gte=weight)
		self.fields['method'].choices = temp
