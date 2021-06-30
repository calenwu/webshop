import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from newsletter.forms import SubscribeForm
from newsletter.models import NewsletterCampaign, Subscriber

from webshop.utils import get_errors_from_form


def unsubscribe_view(request, encoded_email):
	"""
	Unsubscribe from newsletter view
	"""
	subscriber = get_object_or_404(Subscriber, email=Subscriber.decode_email(encoded_email))
	subscriber.delete()
	return render(request, 'newsletter/unsubscribe.html', {'email': subscriber.email})


def subscribe(request):
	"""
		returns {
			'success': true,
		}
		returns {
			'exception': 'You are already subscribed',
		}
	"""
	body_unicode = request.body.decode('utf-8')
	data = json.loads(body_unicode)
	subscriber_form = SubscribeForm(data)
	if subscriber_form.is_valid():
		subscriber_form.save()
		return JsonResponse({
			'success': True,
		})
	else:
		return JsonResponse({
			'exception': get_errors_from_form(subscriber_form)
		})


def popup(request):
	subscriber_form = SubscribeForm()
	x = NewsletterCampaign.objects.filter(active=True)[0]
	return render(request, 'newsletter/popup.html', {
		'newsletter_campaign': x,
		'form': subscriber_form,
	})


def popup_js(request):
	return render(request, 'newsletter/popup_js.html')
