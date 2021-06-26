from django.middleware.csrf import CsrfViewMiddleware

from wagtail.core.views import serve


class CustomCsrfViewMiddleware(CsrfViewMiddleware):
	def process_view(self, request, callback, callback_args, callback_kwargs):
		if callback == serve:
			path = callback_args[0]
			if path.startswith('order/stripe-webhook'):
				return None
		return super().process_view(request, callback, callback_args, callback_kwargs)
