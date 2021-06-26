import logging
import sys
from django.conf import settings
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.payments import CapturesRefundRequest
from paypalcheckoutsdk.orders import OrdersAuthorizeRequest, OrdersCreateRequest, OrdersGetRequest, OrdersPatchRequest
from home.utils import convert_to_paypal_price
from shop.models import Setting as ShopSetting
from order.models import Order, Setting


logger = logging.getLogger('django')


class PayPalClient:
	def __init__(self):
		self.client_id = Setting.get_PAYPAL_CLIENT_ID()
		self.client_secret = Setting.get_PAYPAL_SECRET_KEY()

		"""
		Set up and return PayPal Python SDK environment with PayPal access credentials.
		This sample uses SandboxEnvironment. In production, use LiveEnvironment.
		"""
		if settings.DEBUG:
			self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
		else:
			self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)

		"""
		Returns PayPal HTTP client instance with environment that has access
		credentials context. Use this instance to invoke PayPal APIs, provided the
		credentials have access.
		"""
		self.client = PayPalHttpClient(self.environment)

	def object_to_json(self, json_data):
		"""
		Function to print all json data in an organized readable manner
		"""
		result = {}
		if sys.version_info[0] < 3:
			itr = json_data.__dict__.iteritems()
		else:
			itr = json_data.__dict__.items()
		for key, value in itr:
			# Skip internal attributes.
			if key.startswith("__"):
				continue
			result[key] = self.array_to_json_array(value) if isinstance(value, list) else \
				self.object_to_json(value) if not self.is_primittive(value) else value
		return result

	def array_to_json_array(self, json_array):
		result = []
		if isinstance(json_array, list):
			for item in json_array:
				result.append(self.object_to_json(item) if not self.is_primittive(item)
											else self.array_to_json_array(item) if isinstance(item, list) else item)
		return result

	def is_primittive(self, data):
		return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)

	def create_order(self, order: Order):
		self.check_for_new_keys()
		currency_code = ShopSetting.get_CURRENCY_CODE_PAYPAL()
		request = OrdersCreateRequest()
		request.prefer('return=representation')
		# 3. Call PayPal to set up a transaction
		items = []
		for order_item in order.order_items.all():
			items.append({
				'name': order_item.name,
				'description': '{} / {}'.format(order_item.color, order_item.size),
				'sku': order_item.sku,
				'unit_amount': {
					'currency_code': currency_code,
					'value': convert_to_paypal_price(order_item.get_price())
				},
				'quantity': order_item.quantity
			})
		request.request_body({
			'intent': 'CAPTURE',
			'purchase_units': [
				{
					'reference_id': 'default',
					'custom_id': order.id,
					'description': 'Order ',
					'soft_descriptor': 'Order ',
					'amount': {
						'currency_code': currency_code,
						'value': convert_to_paypal_price(order.get_total_price()),
						'breakdown': {
							'item_total': {
								'currency_code': currency_code,
								'value': convert_to_paypal_price(order.get_pre_sum()),
							},
							'discount': {
								'currency_code': currency_code,
								'value': convert_to_paypal_price(order.get_discount())
							},
							'shipping': {
								'currency_code': currency_code,
								'value': convert_to_paypal_price(order.shipping_method_price),
							},
						}
					},
					'items': items,
					'shipping': {
						'method': order.shipping_method_name,
						'address': {
							'name': {
								'full_name': order.first_name,
								'surname': order.last_name
							},
							'address_line_1': order.address,
							'address_line_2': order.address2,
							'admin_area_1': order.state,
							'admin_area_2': order.city,
							'postal_code': order.postal_code,
							'country_code': order.country
						}
					}
				}
			]
		})
		response = self.client.execute(request)
		return response

	def get_order(self, order_id) -> str:
		"""
		You can use this function to retrieve an order by passing order ID as an argument
		Method to get order
		Returns True if order is completed
		"""
		self.check_for_new_keys()
		request = OrdersGetRequest(order_id)
		response = self.client.execute(request)
		logger.info('Status Code: {}'.format(response.status_code))
		logger.info('Status: {}'.format(response.result.status))
		logger.info('Order ID: '.format(response.result.id))
		logger.info('Intent: '.format(response.result.intent))
		for link in response.result.links:
			logger.info('Link: {}: {}Call Type: {}'.format(link.rel, link.href, link.method))
			logger.info('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
					response.result.purchase_units[0].amount.value))
		if response.result.status == 'COMPLETED':
			return response.result.purchase_units[0].custom_id
		return None

	def order_details(self, order_id):
		"""
		You can use this function to retrieve an order by passing order ID as an argument
		Method to get order
		Returns True if order is completed
		"""
		self.check_for_new_keys()
		request = OrdersGetRequest(order_id)
		response = self.client.execute(request)
		return response.result

	def refund_order(self, order_id: str, amount: float, debug=False):
		"""
		Use the following function to refund an capture. Pass a valid capture ID as an argument.
		"""
		self.check_for_new_keys()
		order_det = self.order_details(order_id)
		capture_id = order_det.purchase_units[0].payments.captures[0].id
		currency_code = order_det.purchase_units[0].payments.captures[0].amount.currency_code
		request = CapturesRefundRequest(capture_id)
		request.prefer("return=representation")
		request.request_body({
			'amount': {
				'value': str(amount),
				'currency_code': currency_code
			}
		})
		response = self.client.execute(request)
		if debug:
			for link in response.result.links:
				print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
			json_data = self.object_to_json(response.result)
			logger.info(json_data)
		return response

	def cancel_order(self, order, order_id):
		"""Method to patch order"""
		self.check_for_new_keys()
		currency_code = ShopSetting.get_CURRENCY_CODE()
		items = []
		for order_item in order.order_items.all():
			items.append({
				'name': order_item.name,
				'description': '{} / {}'.format(order_item.color, order_item.size),
				'sku': order_item.sku,
				'unit_amount': {
					'currency_code': currency_code,
					'value': convert_to_paypal_price(order_item.get_price())
				},
				'quantity': order_item.quantity
			})
		request = OrdersPatchRequest(order_id)
		request.request_body([
			{
				'op': 'replace',
				'path': '/intent',
				'value': 'CAPTURE'
			}, {
				'op': 'replace',
				'path': "/purchase_units/@reference_id=='default'/amount",
				'value': {
					'currency_code': currency_code,
					'value': convert_to_paypal_price(order.get_pre_sum() + 99999999),
					'breakdown': {
						'item_total': {
							'currency_code': currency_code,
							'value': convert_to_paypal_price(order.get_pre_sum()),
						},
						'shipping': {
							'currency_code': currency_code,
							'value': convert_to_paypal_price(99999999),
						},
					}
				}
			}
		])
		#3. Call PayPal to patch the transaction
		self.client.execute(request)
		response = self.client.execute(OrdersGetRequest(order_id))
		logger.info('Status Code: {}'.format(response.status_code))
		logger.info('Status: {}'.format(response.result.status))
		logger.info('Order ID: '.format(response.result.id))
		logger.info('Intent: '.format(response.result.intent))
		for link in response.result.links:
			logger.info('Link: {}: {}Call Type: {}'.format(link.rel, link.href, link.method))
			logger.info('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
					response.result.purchase_units[0].amount.value))

	def check_for_new_keys(self):
		new_keys = False
		if self.client_secret != Setting.get_PAYPAL_SECRET_KEY():
			self.client_secret = Setting.get_PAYPAL_SECRET_KEY()
			new_keys = True
		if self.client_id != Setting.get_PAYPAL_CLIENT_ID():
			self.client_id = Setting.get_PAYPAL_CLIENT_ID()
			new_keys = True
		if new_keys:
			if settings.DEBUG:
				self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
			else:
				self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)
			self.client = PayPalHttpClient(self.environment)
