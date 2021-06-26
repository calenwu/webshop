from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import Footer, FooterItem, HomePage, InformationBar, Menu, MenuItem, TextPage


@register(HomePage)
class HomePageTr(TranslationOptions):
	"""
	State variable translation fields
	"""
	fields = ['content', ]


@register(TextPage)
class TextPageTr(TranslationOptions):
	"""
	State variable translation fields
	"""
	fields = ['body', ]


@register(InformationBar)
class InformationBarTr(TranslationOptions):
	"""
	State variable translation fields
	"""
	fields = ['text']


@register(Footer)
class FooterTr(TranslationOptions):
	"""
	State variable translation fields
	"""
	fields = ['title']


@register(FooterItem)
class FooterItemTr(TranslationOptions):
	"""
	State variable translation fields
	"""
	fields = ['title']


@register(Menu)
class MenuTr(TranslationOptions):
	"""
	State variable translation fields
	"""
	fields = ['title']


@register(MenuItem)
class MenuItemTr(TranslationOptions):
	"""
	State variable translation fields
	"""
	fields = ['title']
