import logging
import os
import pdfkit
import stripe

from django.conf import settings
from django.template.loader import render_to_string

from coupon.models import CouponType
from home.utils import convert_to_paypal_price
from order.models import Setting
from order.paypal import PayPalClient


logger = logging.getLogger('django')
paypal_client = PayPalClient()


def get_invoice(order) -> bytes:
	logger.info(settings.BASE_URL + Setting.get_INVOICE_LOGO_URL())
	html = render_to_string('order/invoice_pdf.html', {
		'order': order,
		'company_name': Setting.get_INVOICE_COMPANY_NAME(),
		'company_signature': Setting.get_INVOICE_COMPANY_SIGNATURE(),
		'business_id': Setting.get_INVOICE_BUSINESS_ID(),
		'logo': settings.BASE_URL + Setting.get_INVOICE_LOGO_URL(),
		'website': Setting.get_INVOICE_WEBSITE(),
		'email': Setting.get_INVOICE_EMAIL(),
		'tax_percentage': Setting.get_TAX_PERCENTAGE(),
	})
	css = [
		os.path.join(settings.BASE_DIR, 'webshop', 'static', 'css', 'tailwind.css'),
		os.path.join(settings.BASE_DIR, 'webshop', 'static', 'css', 'webshop.css')
	]	
	options = {
		'page-size': 'A4',
		'margin-top': '0.75in',
		'margin-right': '0.75in',
		'margin-bottom': '0.75in',
		'margin-left': '0.75in',
		'encoding': "UTF-8",
	}
	return pdfkit.from_string(html, False, options=options, css=css)


def increase_stock(order):
	for order_item in order.order_items.all():
		product_color_quant = order_item.product_color_quantity
		product_color_quant.quantity += order_item.quantity
		product_color_quant.save()


def reduce_stock(order):
	for order_item in order.order_items.all():
		product_color_quant = order_item.product_color_quantity
		product_color_quant.quantity -= order_item.quantity
		if product_color_quant.quantity < 0:
			logger.error('Stock is below 0, OrderId: {}, ProductId: {}, ProductColorId: {}, ProductSizeName: {}'.format(
				order.id, 
				product_color_quant.product_color.product.id,
				product_color_quant.product_color.id,
				product_color_quant.product_size.name
			))
		product_color_quant.save()


def reduce_coupon(order):
	if order.coupon:
		coupon = order.coupon
		if coupon.coupon_type == CouponType.CREDIT.value:
			coupon.credit_used += order.get_discount()
			if coupon.credit_left == 0:
				coupon.active = False
			if coupon.credit_left < 0:
				logger.error('Coupon credit below 0, OrderId: {}, CouponId: {}, CouponName{}'.format(
					order.id, 
					coupon.id,
					coupon.get_full_name(),
				))
		if coupon.one_time:
			coupon.active = False
		coupon.save()


def refund_stripe(payment_intent: str, amount: int):
	stripe.api_key = Setting.get_STRIPE_SECRET_KEY()
	refund = stripe.Refund.create(
		payment_intent=payment_intent,
		amount=amount,
	)


def refund_paypal(order_id: str, amount: int):
	paypal_client.refund_order(order_id, convert_to_paypal_price(amount))
