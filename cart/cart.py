from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from cart.models import Setting as CartSetting
from coupon.models import Coupon, CouponType
from home.utils import convert_to_paypal_price, display_currency_price
from order.models import Order, ShippingMethod
from shop.models import ProductColorQuantity
from webshop.settings.base import CART_SESSION_ID



err_maximum_order_quantity_exceeded = str(_('The maximum order quantity per item  is  %(quantity)s') %
		{'quantity': CartSetting.get_MAXIMUM_ORDER_QUANTITY()}),


class Cart(object):
	def __init__(self, request: HttpRequest):
		"""
		Initialize the cart
		"""
		self.session = request.session
		cart = self.session.get(CART_SESSION_ID)
		if not cart:
			cart = {
				'items': {},
			}
		self.cart = cart

	def __iter__(self) -> dict:
		"""
		Iterate over the items in the cart and get the products from the database
		"""
		for product_color_quantity_id in self.cart['items'].keys():
			self.set_default_values(product_color_quantity_id)
		for product_color_quantity_id in self.cart['items'].keys():
			self.update_total_price(product_color_quantity_id)
			product_color_quantity = ProductColorQuantity.objects.select_related('product_color').select_related('product_color__product').select_related('product_size').get(id=product_color_quantity_id)
			product_color = product_color_quantity.product_color
			product = product_color.product
			self.cart['items'][product_color_quantity_id]['id'] = product_color_quantity.id
			self.cart['items'][product_color_quantity_id]['link'] = product.link
			self.cart['items'][product_color_quantity_id]['title'] = product.title
			self.cart['items'][product_color_quantity_id]['image_url'] = product.image.file.url
			self.cart['items'][product_color_quantity_id]['variation'] = product_color_quantity.get_display_variation()
			self.cart['items'][product_color_quantity_id]['display_price'] = product.get_display_price()
			self.cart['items'][product_color_quantity_id]['display_total_price'] = display_currency_price(
				self.cart['items'][product_color_quantity_id]['total_price'])
			yield self.cart['items'][product_color_quantity_id]

	def __len__(self) -> int:
		"""
		Counter all items in the cart
		"""
		number_of_items = 0
		for item in self.cart['items']:
			number_of_items += self.cart['items'][item]['quantity']
		return number_of_items

	@property
	def is_good(self) -> bool:
		if len(self) != 0 and self.enough_stock():
			return True
		return False

	@property
	def shipping_method(self) -> ShippingMethod:
		""""""
		shipping_id = self.get_shipping_id()
		if shipping_id:
			weight = self.get_total_weight()
			temp = ShippingMethod.objects.filter(id=shipping_id, active=True, min_weight__lte=weight, max_weight__gte=weight)
			if not temp:
				self.remove_shipping_id()
			else:
				return temp[0]
		return None

	@property
	def coupon(self) -> Coupon:
		"""
		Return the coupon if applied and it is valid, else remove the coupon and return None
		"""
		coupon_id = self.get_coupon_id()
		if coupon_id:
			coupon = Coupon.objects.get(id=coupon_id, active=True)
			if coupon.is_valid():
				return coupon
			self.remove_coupon_id()
		return None

	@property
	def order(self) -> Order:
		"""
		Get the order
		"""
		order_id = self.get_order_id()
		if order_id:
			return Order.objects.get(id=order_id)
		return None

	def set_default_values(self, product_color_quantity_id: str) -> None:
		product_color_quantity_id = str(product_color_quantity_id)
		if product_color_quantity_id not in self.cart['items']:
			self.cart['items'][product_color_quantity_id] = {}
		product_color_quantity = ProductColorQuantity.objects.get(id=product_color_quantity_id)
		product_color = product_color_quantity.product_color
		self.cart['items'][product_color_quantity_id]['product_color_quantity_id'] = product_color_quantity.id
		self.cart['items'][product_color_quantity_id]['product_color_id'] = product_color.id
		self.cart['items'][product_color_quantity_id]['product_size_id'] = product_color_quantity.product_size.id
		self.cart['items'][product_color_quantity_id]['price'] = product_color.product.get_price()
		self.update_total_price(product_color_quantity_id)

	def enough_stock(self) -> bool:
		"""
		If there is enough stock
		"""
		for product_color_quantity_id in self.cart['items'].keys():
			if ProductColorQuantity.objects.get(id=product_color_quantity_id).quantity < \
						self.cart['items'][product_color_quantity_id]['quantity']:
				return False
		return True

	def calc_overflow(self) -> None:
		"""
		calculate which items are overshooting the stock
		"""
		self.cart['available'] = {}
		self.cart['out_of_stock'] = []
		for product_color_quantity_id in self.cart['items'].keys():
			avail_qty = ProductColorQuantity.objects.get(id=product_color_quantity_id).quantity
			cart_qty = self.cart['items'][product_color_quantity_id]['quantity']
			if avail_qty < cart_qty:
				if avail_qty <= 0:
					self.cart['out_of_stock'].append(int(product_color_quantity_id))
				else:
					self.cart['available'][int(product_color_quantity_id)] = avail_qty
		self.save()

	def update_total_price(self, product_color_quantity_id: str) -> None:
		product_color_quantity_id = str(product_color_quantity_id)
		self.cart['items'][product_color_quantity_id]['total_price'] = round(
			self.cart['items'][product_color_quantity_id]['quantity'] *
			self.cart['items'][product_color_quantity_id]['price'],
			2
		)

	def add(self, product_color_quantity: ProductColorQuantity, quantity=1, update_quantity=False) -> dict:
		"""
		Add a product to the cart or update its quantity.
		"""
		maximum_order_quantity = CartSetting.get_MAXIMUM_ORDER_QUANTITY()
		quantity = int(quantity)
		if quantity < 0:
			return {
				'data': {
					'success': True,
					'message': {
						'title': _('Invalid quantity'),
						'innerHtml': _('Please enter a valid quantity.'),
						'tag': 'error'
					}
				}
			}
		product_color_quantity_id = str(product_color_quantity.id)
		if str(product_color_quantity_id) not in self.cart['items']:
			self.cart['items'][product_color_quantity_id] = {'quantity': 0}
			self.set_default_values(product_color_quantity_id)
		if update_quantity:
			if quantity == 0:
				self.remove(product_color_quantity_id)
				return {
					'data': {
						'success': True,
					}
				}
			else:
				self.cart['items'][product_color_quantity_id]['quantity'] = quantity
		else:
			self.cart['items'][product_color_quantity_id]['quantity'] += quantity
		if product_color_quantity.quantity <= 0:
			return {
				'data': {
					'success': True,
					'message': {
						'title': _('Out of stock'),
						'innerHtml': _('Sorry we are out of stock'),
						'tag': 'error'
					}
				}
			}
		if self.cart['items'][product_color_quantity_id]['quantity'] > product_color_quantity.quantity:
			self.cart['items'][product_color_quantity_id]['quantity'] = product_color_quantity.quantity
			if self.cart['items'][product_color_quantity_id]['quantity'] == 0:
				self.remove(product_color_quantity_id)
			else:
				self.update_total_price(product_color_quantity_id)
			self.remove_order_id()
			return {
				'data': {
					'success': True,
					'message': {
						'title': str(_('Only  %(quantity)s left') % {'quantity': product_color_quantity.quantity}),
						'innerHtml': str(_('Sorry we only have  %(quantity)s left in stock') %
								{'quantity': product_color_quantity.quantity}),
						'tag': 'warning'
					}
				}
			}
		if self.cart['items'][product_color_quantity_id]['quantity'] > CartSetting.get_MAXIMUM_ORDER_QUANTITY():
			self.cart['items'][product_color_quantity_id]['quantity'] = CartSetting.get_MAXIMUM_ORDER_QUANTITY()
			if self.cart['items'][product_color_quantity_id]['quantity'] == 0:
				self.remove(product_color_quantity_id)
			else:
				self.update_total_price(product_color_quantity_id)
			self.remove_order_id()
			return {
				'data': {
					'success': True,
					'message': {
						'title': str(_('Exceeded maximum order quantity')),
						'innerHtml': err_maximum_order_quantity_exceeded,
						'tag': 'warning'
					}
				}
			}
		self.remove_order_id()
		return {
			'data': {
				'success': True,
			}
		}

	def remove(self, product_color_quantity_id: str) -> None:
		"""
		Remove a product from the cart
		"""
		product_color_quantity_id = str(product_color_quantity_id)
		if product_color_quantity_id in self.cart['items'].keys():
			del self.cart['items'][product_color_quantity_id]
		self.remove_order_id()

	def get_pre_coupon_price(self) -> int:
		"""
		Get the total price of the cart
		"""
		total_price = 0
		for item in self.cart['items'].values():
			total_price += item['price'] * item['quantity']
		return total_price

	def get_display_pre_coupon_price(self) -> str:
		"""
		Get the total price of the cart before discount
		"""
		return display_currency_price(self.get_pre_coupon_price())

	def get_discount(self) -> int:
		"""
		Get the discounted amount
		"""
		if self.get_coupon_id():
			coupon = self.coupon
			if coupon.coupon_type == CouponType.PERCENTAGE.value:
				return int((coupon.percentage / 100) * self.get_pre_coupon_price())
			if coupon.coupon_type == CouponType.CREDIT.value:
				return coupon.credit_left if coupon.credit_left <= self.get_pre_coupon_price() else self.get_pre_coupon_price()
		return 0

	def get_display_discount(self) -> str:
		"""
		Get the total discount
		"""
		return display_currency_price(self.get_discount())

	def get_price_pre_shipping(self) -> int:
		"""
		Get the discounted price
		"""
		return self.get_pre_coupon_price() - self.get_discount()

	def get_display_price_pre_shipping(self) -> int:
		"""
		Get the discounted price
		"""
		return display_currency_price(self.get_price_pre_shipping())

	def get_total_price(self) -> int:
		"""
		Get the discounted price
		"""
		temp = self.shipping_method
		t = 0
		if temp:
			t = temp.get_price()
		return self.get_price_pre_shipping() + t

	def get_display_total_price(self) -> str:
		"""
		Get the total price of the cart after discount
		"""
		return display_currency_price(self.get_total_price())

	def get_stripe_charge_amount(self) -> int:
		"""
		Get the stripe charge amount
		"""
		return self.get_total_price()

	def get_paypal_charge_amount(self) -> str:
		"""
		Get the paypal charge amount
		"""
		return convert_to_paypal_price(self.get_total_price())

	def get_total_weight(self) -> int:
		"""
		Get total weight of the items
		"""
		weight = 0
		for product_color_quantity_id in self.cart['items'].keys():
			weight += ProductColorQuantity.objects.get(id=product_color_quantity_id).product_color.product.weight * \
					self.cart['items'][product_color_quantity_id]['quantity']
		return round(weight, 2)

	def get_coupon_id(self) -> int:
		if 'coupon_id' in self.cart:
			return self.cart['coupon_id']
		return None

	def set_coupon_id(self, coupon_id) -> None:
		self.cart['coupon_id'] = coupon_id
		self.remove_order_id()
		self.save()

	def remove_coupon_id(self) -> None:
		self.cart.pop('coupon_id', None)
		self.remove_order_id()
		self.save()

	def get_shipping_id(self) -> int:
		if 'shipping_id' in self.cart:
			return self.cart['shipping_id']
		return None

	def set_shipping_id(self, shipping_method_id: int) -> None:
		self.cart['shipping_id'] = shipping_method_id
		self.save()

	def remove_shipping_id(self) -> None:
		self.cart.pop('shipping_id', None)
		self.save()

	def get_order_id(self) -> int:
		if 'order_id' in self.cart:
			return self.cart['order_id']
		return None

	def set_order_id(self, order_id: int) -> None:
		self.cart['order_id'] = order_id
		self.save()

	def remove_order_id(self) -> None:
		self.cart.pop('order_id', None)
		self.save()

	def save(self) -> None:
		"""
		Update the session cart
		"""
		self.session[CART_SESSION_ID] = self.cart
		self.session.modified = True

	def clear(self) -> None:
		"""
		Empty the cart
		"""
		self.session[CART_SESSION_ID] = {}
		self.session.modified = True
