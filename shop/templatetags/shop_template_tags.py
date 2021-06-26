from django import template
from shop.models import ProductPage, ProductColor, ProductSize, ProductColorQuantity, Setting


register = template.Library()


@register.simple_tag
def increment(val):
	return val + 1

@register.simple_tag
def increment_by(val, increase_by):
	return val + increase_by

@register.simple_tag
def get_product(id):
	return ProductPage.objects.get(id=id)

@register.simple_tag
def get_product_color(id):
	return ProductColor.objects.get(id=id)

@register.simple_tag
def get_product_color_quantity(id):
	return ProductColorQuantity.objects.get(id=id)

@register.simple_tag
def get_product_size(id):
	return ProductSize.objects.get(id=id)

@register.simple_tag
def get_currency():
	return Setting.get_CURRENCY()

@register.simple_tag
def get_currency_code_paypal():
	return Setting.get_CURRENCY_CODE_PAYPAL()

@register.simple_tag
def get_currency_stripe():
	return Setting.get_CURRENCY_CODE_STRIPE()
