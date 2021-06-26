from modeltranslation.translator import translator, TranslationOptions
from .models import Country, State, Setting, ShippingMethod


class CountryOptions(TranslationOptions):
	"""
	Country translation fields
	"""
	fields = ['name']


class StateOptions(TranslationOptions):
	"""
	State variable translation fields
	"""
	fields = ['name']


class SettingOptions(TranslationOptions):
	"""
	State variable translation fields
	"""
	fields = ['value']


class ShippingMethodOptions(TranslationOptions):
	"""
	State variable translation fields
	"""
	fields = ['name', 'description']


translator.register(Country, CountryOptions)
translator.register(State, StateOptions)
translator.register(Setting, SettingOptions)
translator.register(ShippingMethod, ShippingMethodOptions)
