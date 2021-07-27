from __future__ import absolute_import, unicode_literals
import logging
import stripe
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from celery import shared_task

from order.models import Order, Setting
from order.paypal import PayPalClient
from order.utils import get_invoice, increase_stock


logger = logging.getLogger('django')
paypal_client = PayPalClient()


@shared_task
def save_invoice(order_id) -> None:
	order = Order.objects.get(id=order_id)
	f = open('{}/order/media/invoices/{}.pdf'.format(settings.BASE_DIR, order.invoice_number), 'wb')
	f.write(get_invoice(order))
	f.close()


@shared_task
def send_invoice(order_id) -> None:
	order = Order.objects.get(id=order_id)
	subject = Setting.get_ORDER_CONFIRMATION_SUBJECT() + ' - ' + order.order_number
	url = reverse('order:view', args=[order.url])
	html_content = render_to_string('order/email/order.html',  {
		'first_name': order.first_name,
		'shop_link': settings.BASE_URL,
		'order_link': settings.BASE_URL + url[3:len(url)],
		'email_button_color': Setting.get_EMAIL_BUTTON_COLOR(),
		'email_button_text_color': Setting.get_EMAIL_BUTTON_TEXT_COLOR(),
	})
	text_content = strip_tags(html_content)
	email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, (order.email, ))
	email.attach_alternative(html_content, 'text/html')
	email.attach('order_{}.pdf'.format(order.invoice_number), get_invoice(order), 'application/pdf')
	return email.send()


@shared_task
def send_shipping_notification(order_id) -> None:
	order = Order.objects.get(id=order_id)
	subject = Setting.get_SHIPPING_CONFIRMATION_SUBJECT() + ' - ' + order.order_number
	html_content = render_to_string('order/email/shipping.html', {
		'first_name': order.first_name,
		'shop_link': settings.BASE_URL,
		'tracking_link': order.tracking_number_link,
		'email_button_color': Setting.get_EMAIL_BUTTON_COLOR(),
		'email_button_text_color': Setting.get_EMAIL_BUTTON_TEXT_COLOR(),
	})
	text_content = strip_tags(html_content)
	email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, (order.email, ))
	email.attach_alternative(html_content, 'text/html')
	return email.send()


@shared_task
def check_if_order_paid(order_id, payment_intent_id, paypal_order_id) -> None:
	order = Order.objects.get(id=order_id)
	if not order.paid:
		logger.info('canceled')
		increase_stock(order)
		stripe.api_key = Setting.get_STRIPE_SECRET_KEY()
		stripe.PaymentIntent.cancel(payment_intent_id)
		paypal_client.cancel_order(order, paypal_order_id)


@shared_task
def reduce_stock(order_id):
	order = Order.objects.get(id=order_id)
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