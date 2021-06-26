import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from cart.cart import Cart

from shop.models import ProductListingsPage, ProductColorQuantity


def add(request, product_color_quantity_id: str, quantity: str):
	"""
	Add product to cart
	"""
	cart = Cart(request)
	try:
		quantity = int(quantity)
		if quantity < 1:
			return JsonResponse({
				'data': {
					'success': False,
					'message': {
						'title': str(_('Error while adding to cart')),
						'innerHtml': str(_('Please enter a number greater than 0')),
						'tag': 'error'
					}
				}
			})
		product_color_quantity = ProductColorQuantity.objects.get(id=product_color_quantity_id)
		return JsonResponse(cart.add(
			product_color_quantity=product_color_quantity,
			quantity=quantity,
			update_quantity=False
		))
	except ProductColorQuantity.DoesNotExist:
		return JsonResponse({
			'data': {
				'success': False,
				'message': {
					'title': str(_('Error while adding to cart')),
					'innerHtml': str(_('There is no product with the id %(product_color_quantity_id)') %
							{'product_color_quantity_id': product_color_quantity_id}),
					'tag': 'error'
				}
			}
		})
	except ValueError:
		return JsonResponse({
			'data': {
				'success': False,
				'message': {
					'title': str(_('Error while adding to cart')),
					'innerHtml': str(_('Please enter a valid number')),
					'tag': 'error'
				}
			}
		})
	except Exception as ex:
		return JsonResponse({
			'data': {
				'success': False,
				'message': {
					'title': str(_('Error while adding to cart')),
					'innerHtml': str(ex),
					'tag': 'error'
				}
			}
		})


def update(request, product_color_quantity_id: str, quantity: str):
	"""
	Update quantity of a ProductColorQuantity in cart
	"""
	cart = Cart(request)
	try:
		quantity = int(quantity)
		if quantity < 0:
			return JsonResponse({
				'data': {
					'success': False,
					'message': {
						'title': str(_('Error while updating cart')),
						'innerHtml': str(_('Please enter a number greater than 0')),
						'tag': 'error'
					}
				}
			})
		product_color_quantity = ProductColorQuantity.objects.get(id=product_color_quantity_id)
		return JsonResponse(cart.add(
			product_color_quantity=product_color_quantity,
			quantity=quantity,
			update_quantity=True
		))
	except ProductColorQuantity.DoesNotExist:
		return JsonResponse({
			'data': {
				'success': False,
				'message': {
					'title': str(_('Error while updating cart')),
					'innerHtml': str(_('There is no product with the id %(product_color_quantity_id)') %
							{'product_color_quantity_id': product_color_quantity_id}),
					'tag': 'error'
				}
			}
		})
	except ValueError:
		return JsonResponse({
			'data': {
				'success': False,
				'message': {
					'title': str(_('Error while updating cart')),
					'innerHtml': str(_('Please enter a valid number')),
					'tag': 'error'
				}
			}
		})
	except Exception as ex:
		return JsonResponse({
			'data': {
				'success': False,
				'message': {
					'title': str(_('Error while updating cart')),
					'innerHtml': str(ex),
					'tag': 'error'
				}
			}
		})


def cart_overlay_content(request):
	cart = Cart(request)
	return render(request, 'cart/cart_overlay.html', {
		'cart': cart,
		'products_url': ProductListingsPage.objects.all()[0].link
	})


def cart_checkout_top(request):
	cart = Cart(request)
	return render(request, 'cart/cart_checkout_top.html', {
		'cart': cart,
	})


def cart_checkout_right(request):
	cart = Cart(request)
	return render(request, 'cart/cart_checkout_right.html', {
		'cart': cart,
	})


def details(request):
	cart = Cart(request)
	available = {}
	out_of_stock = []
	if not cart.is_good and len(cart) != 0:
		cart.calc_overflow()
		available = cart.cart['available']
		out_of_stock = cart.cart['out_of_stock']
		messages.error(
			request, 
			json.dumps({
				'data': {
					'title': str(_('Update cart')),
					'innerHTML': str(_('There is not enough stock available for your order, please update your cart.')),
					'type': 'error'
				}
			})
		)
	return render(request, 'cart/details.html', {
		'cart': cart,
		'available': available,
		'available_keys': list(available.keys()),
		'out_of_stock': out_of_stock,
		'products_url': ProductListingsPage.objects.all()[0].link,
	})
