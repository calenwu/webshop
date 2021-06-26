from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST

from cart.cart import Cart
from coupon.models import Coupon


@csrf_protect
@require_POST
def apply(request):
	"""
	Coupon form view
	"""
	cart = Cart(request)
	now = timezone.now()
	coupon = Coupon.objects.filter(
		code__iexact=request.POST.get('code', ''), valid_from__lte=now, valid_to__gte=now, active=True)
	if coupon:
		cart.set_coupon_id(coupon[0].id)
		return JsonResponse({
			'data': {
				'success': True, 
			}
		})
	return JsonResponse({
		'data': {
			'success': False, 
			'message': {
				'title': str(_('Invalid Code')),
				'innerHtml': str(_('The code you entered seems to be invalid')),
				'tag': 'error'
			}
		}
	})


@require_POST
@csrf_exempt
def remove(request):
	"""
	Coupon form view
	"""
	cart = Cart(request)
	cart.remove_coupon_id()
	return JsonResponse({
		'data': {
			'success': True, 
		}
	})
