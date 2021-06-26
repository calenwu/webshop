from django import template
from cart.forms import AddProductToCartForm, ChangeProductQuantityForm
from home.utils import display_currency_price
from shop.models import Setting as ShopSetting
from order.models import ShippingMethod


register = template.Library()


@register.simple_tag
def get_add_product_form(product_color_quantity_id):
	return AddProductToCartForm(product_color_quantity_id)


@register.simple_tag
def get_update_quantity_form(cart_item):
	return ChangeProductQuantityForm(initial={'quantity': cart_item['quantity'], 'update': True})


@register.simple_tag
def get_shipping_method(shipping_id):
	try:
		return ShippingMethod.objects.get(id=shipping_id)
	except Exception:
		return None


@register.simple_tag
def get_display_currency_price(s: str) -> str:
	return display_currency_price(s)


@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)
