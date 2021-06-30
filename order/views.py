import json
import logging
import stripe

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt

from account.utils import get_user_from_request
from cart.cart import Cart
from order.forms import AddressForm, OrderCreateForm, ShippingForm
from order.models import Order, OrderItem, OrderStatus, ShippingMethod, State, Setting
from order.order import Order as OrderSession
from order.paypal import PayPalClient
from order.utils import get_invoice, reduce_coupon, reduce_stock
from order.tasks import check_if_order_paid, save_invoice, send_invoice
from shop.models import ProductColorQuantity, Setting as ShopSetting


logger = logging.getLogger('django')
paypal_client = PayPalClient()
stripe.api_key = Setting.get_STRIPE_SECRET_KEY()


def information(request):
	"""
	Set customer information for order view
	"""
	user = get_user_from_request(request)
	cart = Cart(request)
	order = OrderSession(request)
	initial_data = {}
	if user:
		if user.address.all():
			address = user.address.all()[0]
			initial_data = {
				'email': address.email, 
				'first_name': address.first_name, 
				'last_name': address.last_name, 
				'company': address.company, 
				'address': address.address, 
				'address2': address.address2,  
				'city': address.city,  
				'country': address.country,  
				'state': address.state,  
				'postal_code': address.postal_code, 
				'telephone': address.telephone,
			}
			order.set_address(initial_data)
	form = OrderCreateForm(initial=initial_data)
	if cart.is_good:
		if request.method == 'POST':
			form = OrderCreateForm(request.POST)
			if form.is_valid():
				order.set_address(form.cleaned_data)
				if user:
					updated_request = request.POST.copy()
					updated_request.update({'user': user.id})
					address = AddressForm(user.id, updated_request)
					if address.is_valid():
						address.save()
						if not user.first_name:
							user.first_name = address.cleaned_data['first_name']
							user.last_name = address.cleaned_data['last_name']
							user.save()
						pass
				request.session['shipping'] = True
				return redirect(reverse('order:shipping'))
	else:
		return redirect(reverse('cart:details'))
	return render(request, 'order/information.html', {
		'cart': cart,
		'form': form,
		'order': order,
		'states': json.dumps(State.get_dict())
	})


def shipping(request):
	"""
	Set customer information for order view
	"""
	cart = Cart(request)
	order = OrderSession(request)
	if not request.session.get('shipping'):
		return redirect(reverse('order:information'))
	if not cart.is_good:
		return redirect(reverse('cart:details'))
	if request.method == 'POST':
		shipping_form = ShippingForm(cart.get_total_weight(), request.POST)
		if shipping_form.is_valid():
			cart.set_shipping_id(shipping_form.cleaned_data['method'].id)
			return redirect(reverse('order:payment'))
		else:
			return render(request, 'order/shipping.html', {
				'cart': cart,
				'order': order.order,
				'form': shipping_form
			})
	return render(request, 'order/shipping.html', {
		'cart': cart,
		'order': order.order,
		'form': ShippingForm(cart.get_total_weight())
	})


def payment(request):
	cart = Cart(request)
	order_session = OrderSession(request)
	shipping_method = cart.shipping_method
	if not shipping_method:
		return redirect(reverse('order:shipping'))
	if not cart.is_good:
		return redirect(reverse('cart:details'))
	user = get_user_from_request(request)
	order = None
	if cart.order and not cart.order.paid:
		order = cart.order
	else:
		coupon = cart.coupon
		order = Order.objects.create(
			user=user,
			url=Order.generate_random_string(),
			email=order_session.order['email'],
			first_name=order_session.order['first_name'],
			last_name=order_session.order['last_name'],
			company=order_session.order['company'],
			address=order_session.order['address'],
			address2=order_session.order['address2'],
			postal_code=order_session.order['postal_code'],
			country=order_session.order['country'],
			city=order_session.order['city'],
			state=order_session.order['state'],
			telephone=order_session.order['telephone'],
			comment=order_session.order['comment'],
			shipping_method=shipping_method,
			shipping_method_name=shipping_method.get_full_name(),
			shipping_method_price=shipping_method.get_price(),
			paid=False,
			coupon=coupon,
			coupon_name=coupon.get_full_name() if coupon else None,
			discount=cart.get_discount(),
		)
	order_items = []
	for item in cart:
		product_color_quantity = ProductColorQuantity.objects.get(id=item['product_color_quantity_id'])
		product_color = product_color_quantity.product_color
		order_items.append(
			OrderItem.objects.create(
				order=order,
				product_color_quantity=product_color_quantity,
				sku=product_color.id,
				name=product_color.product.title,
				price=product_color.product.get_price(),
				color=product_color.color,
				quantity=item['quantity'],
				size=product_color_quantity.product_size.name,
			)
		)
	stripe_payment_intent = create_stripe_payment_intent(order)
	paypal_order_id = paypal_client.create_order(order).result['id']
	reduce_stock(order)
	check_if_order_paid.apply_async(
		(order.id, stripe_payment_intent.id, paypal_order_id), 
		countdown=Setting.get_CHECKOUT_TIMEOUT())
	return render(request, 'order/payment.html', {
		'cart': cart,
		'order': order,
		'order_items': order_items,
		'shipping_method': shipping_method,
		'stripe_publishable_key': Setting.get_STRIPE_PUBLISHABLE_KEY(),
		'paypal_client_id': Setting.get_PAYPAL_CLIENT_ID(),
		'stripe_payment_intent_client_secret': stripe_payment_intent.client_secret,
		'paypal_order_id': paypal_order_id
	})


def create_stripe_payment_intent(order) -> stripe.PaymentIntent:
	try:
		set_stripe_api_key()
		return stripe.PaymentIntent.create(
			amount=order.get_total_price(),
			currency=ShopSetting.get_CURRENCY_CODE_STRIPE(),
			payment_method_types=['card', 'sofort'],
			payment_method_options={
				'sofort': {
					'preferred_language': translation.get_language(),
				},
			},
			metadata={
				'order_id': str(order.id),
			},
			shipping={
				'address': {
					'city': order.city,
					'country': order.country,
					'line1': order.address,
					'line2': order.address2,
					'postal_code': order.postal_code,
					'state': order.state
				},
				'name': order.first_name + ' ' + order.last_name,
				'phone': order.telephone,
				'carrier': '',
				'tracking_number': '',
			}
		)
	except Exception as e:
		logger.error(e)
		raise e


@csrf_exempt
def stripe_webhook(request):
	payload = request.body
	event = None
	try:
		set_stripe_api_key()
		event = stripe.Event.construct_from(
			json.loads(payload), stripe.api_key
		)
	except stripe.error.CardError as e:
		# Since it's a decline, stripe.error.CardError will be caught
		logger.error('Status is: %s' % e.http_status)
		logger.error('Code is: %s' % e.code)
		# param is '' in this case
		logger.error('Param is: %s' % e.param)
		logger.error('Message is: %s' % e.user_message)
	except stripe.error.RateLimitError as e:
		# Too many requests made to the API too quickly
		logger.error('Too many requests made to the API too quickly: ' + e)
		return HttpResponse(status=400)
	except stripe.error.InvalidRequestError as e:
		# Invalid parameters were supplied to Stripe's API
		logger.error("Invalid parameters were supplied to Stripe's API: " + e)
		return HttpResponse(status=400)
	except stripe.error.AuthenticationError as e:
		# Authentication with Stripe's API failed
		# (maybe you changed API keys recently)
		logger.error("Authentication with Stripe's API failed (maybe you changed API keys recently): " + e)
		return HttpResponse(status=400)
	except stripe.error.APIConnectionError as e:
		# Network communication with Stripe failed
		logger.error('Network communication with Stripe failed: ' + e)
		return HttpResponse(status=400)
	except stripe.error.StripeError as e:
		# Display a very generic error to the user, and maybe send
		# yourself an email
		logger.error('Display a very generic error to the user, and maybe send yourself an email: ' + e)
		return HttpResponse(status=400)
	except ValueError as e:
		# Invalid payload
		return HttpResponse(status=400)
	except Exception as e:
		# Something else happened, completely unrelated to Stripe
		logger.error('Error: ' + str(e))
		return HttpResponse(status=400)
	# Handle the event
	if event.type == 'payment_intent.succeeded':
		payment_intent = event.data.object
		order = Order.objects.get(id=payment_intent['metadata']['order_id'])
		if not order.paid:
			order_processed(order, stripe_payment_id=payment_intent.stripe_id)
	elif event.type == 'payment_method.attached':
		payment_method = event.data.object  # contains a stripe.PaymentMethod
		logger.error('PaymentMethod was attached to a Customer!')
	# ... handle other event types
	else:
		logger.error('Unhandled event type {}'.format(event.type))
	return HttpResponse(status=200)


def stripe_verification(request, payment_intent_id):
	payment_intent = None
	try:
		set_stripe_api_key()
		payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
	except stripe.error.CardError as e:
		# Since it's a decline, stripe.error.CardError will be caught
		logger.error('Status is: %s' % e.http_status)
		logger.error('Code is: %s' % e.code)
		# param is '' in this case
		logger.error('Param is: %s' % e.param)
		logger.error('Message is: %s' % e.user_message)
	except stripe.error.RateLimitError as e:
		# Too many requests made to the API too quickly
		logger.error('Too many requests made to the API too quickly: ' + e)
	except stripe.error.InvalidRequestError as e:
		# Invalid parameters were supplied to Stripe's API
		logger.error("Invalid parameters were supplied to Stripe's API: " + e)
	except stripe.error.AuthenticationError as e:
		# Authentication with Stripe's API failed
		# (maybe you changed API keys recently)
		logger.error("Authentication with Stripe's API failed (maybe you changed API keys recently): " + e)
	except stripe.error.APIConnectionError as e:
		# Network communication with Stripe failed
		logger.error('Network communication with Stripe failed: ' + e)
	except stripe.error.StripeError as e:
		# Display a very generic error to the user, and maybe send
		# yourself an email
		logger.error('Display a very generic error to the user, and maybe send yourself an email: ' + e)
	except Exception as e:
		# Something else happened, completely unrelated to Stripe
		logger.error('Error: ' + str(e))
	if payment_intent['amount'] == payment_intent['amount_received']:
		order = Order.objects.get(id=payment_intent['metadata']['order_id'])
		order_processed(order, stripe_payment_id=payment_intent.stripe_id)
		Cart(request).clear()
		OrderSession(request).clear()
		return JsonResponse({
			'data': {
				'success': True,
				'url': reverse('order:view', args=[order.url])
			}
		})
	return JsonResponse({
		'data': {
			'success': False,
		}
	})


def paypal_verification(request, paypal_order_id):
	"""
	Paypal verification view
	"""
	order_id = False
	try:
		order_id = paypal_client.get_order(paypal_order_id)
	except stripe.error.CardError as e:
		# Since it's a decline, stripe.error.CardError will be caught
		logger.error('Status is: %s' % e.http_status)
		logger.error('Code is: %s' % e.code)
		# param is '' in this case
		logger.error('Param is: %s' % e.param)
		logger.error('Message is: %s' % e.user_message)
	except Exception as e:
		logger.error('Error: ' + str(e))
		pass
	if order_id:
		order = Order.objects.get(id=order_id)
		if not order.paid:
			order_processed(order, paypal_order_id=paypal_order_id)
			Cart(request).clear()
			OrderSession(request).clear()
		return JsonResponse({
			'data': {
				'success': True,
				'url': reverse('order:view', args=[order.url])
			}
		})
	return JsonResponse({
		'data': {
			'success': False,
			'url': reverse('order:payment')
		}
	})


@csrf_exempt
def paypal_webhook(request):
	try:
		payload = json.loads(request.body)
		order = Order.objects.get(id=payload['resource']['custom_id'])
		if not order.paypal_order_id:
			if payload['resource']['status'] == 'CAPTURED':
				order_processed(order, paypal_order_id=payload['resource']['id'])
	except Exception as e:
		logger.error('Error: ' + str(e))
		return HttpResponse(status=400)
	return HttpResponse(status=200)


def view(request, order_url):
	order = Order.objects.get(url=order_url)
	return render(request, 'order/view.html', {
		'order': order
	})


# useless I think
@staff_member_required
def invoice_pdf(request, order_id):
	"""
	Invoice as html view
	"""
	order = get_object_or_404(Order, id=order_id)
	response = HttpResponse(get_invoice(order), content_type='application/pdf')
	response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.invoice_number)
	return response


# useless I think
@staff_member_required
def confirmation_email(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	url = reverse('order:view', args=[order.url])
	return render(request, 'order/email/order.html', {
		'first_name': order.first_name,
		'shop_link': settings.BASE_URL,
		'order_link': settings.BASE_URL + url[3:len(url)],
	})


# useless I think
@staff_member_required
def shipping_email(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	url = reverse('order:view', args=[order.url])
	return render(request, 'order/email/shipping.html', {
		'first_name': order.first_name,
		'shop_link': settings.BASE_URL,
		'order_link': settings.BASE_URL + url[3:len(url)],
	})


@staff_member_required
def admin_order_detail(request, order_id):
	"""
	Detailed order view for admin
	"""
	order = get_object_or_404(Order, id=order_id)
	return render(request, 'order/admin/detail.html', {'order': order})


def order_processed(order, stripe_payment_id=None, paypal_order_id=None):
	"""
	All necessary steps after payment was captured
	"""
	if not stripe_payment_id and not paypal_order_id:
		raise ValueError('Need to pass either stripe_payment_id or paypal_order_id')
	if stripe_payment_id:
		order.stripe_id = stripe_payment_id
	else:
		order.paypal_order_id = paypal_order_id
	order.status = OrderStatus.PROCESSING
	order.paid = True
	order.unique_paid_number = Order.generate_unique_paid_number()
	order.save()
	reduce_coupon(order)
	save_invoice.delay(order.id)
	send_invoice.delay(order.id)

def set_stripe_api_key():
	if stripe.api_key != Setting.get_STRIPE_SECRET_KEY():
		stripe.api_key = Setting.get_STRIPE_SECRET_KEY()
