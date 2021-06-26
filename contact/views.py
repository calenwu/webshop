import json
import re
import requests

from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from contact.models import Setting
from contact.forms import ContactForm


def contact_view(request):
	"""
	Contact view
	"""
	contact_form = ContactForm()
	if request.method == 'POST':
		if not request.POST['g-recaptcha-response']:
			messages.error(
				request,
				json.dumps({
					'data': {
						'title': str(_('Message not sent')),
						'innerHTML': str(_('Please complete the captcha')),
						'type': 'error'
					}
				})
			)
			return render(request, 'contact/contact.html', {
				'contact_form': ContactForm(),
				'site_key': Setting.get_RECAPTCHA_PUBLIC_KEY(),
			})
		data = {
			'response': request.POST['g-recaptcha-response'],
			'secret': Setting.get_RECAPTCHA_PRIVATE_KEY(),
		}
		resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
		result_json = resp.json()
		if not result_json.get('success'):
			messages.error(
				request,
				json.dumps({
					'data': {
						'title': str(_('Message not sent')),
						'innerHTML': str(_('We think that you are a robot')),
						'type': 'error'
					}
				})
			)
			return render(request, 'contact/contact.html', {
				'contact_form': ContactForm(),
				'site_key': Setting.get_RECAPTCHA_PUBLIC_KEY(),
			})
		contact_form = ContactForm(data=request.POST)
		if contact_form.is_valid():
			contact_form.save()
			messages.success(
				request,
				json.dumps({
					'data': {
						'title': str(_('Message sent')),
						'innerHTML': str(_('We received your message and will respond as soon as possible')),
						'type': 'success'
					}
				})
			)
		else:
			messages.error(
				request,
				json.dumps({
					'data': {
						'title': str(_('Message not sent')),
						'innerHTML': get_errors_from_form(contact_form),
						'type': 'error'
					}
				})
			)
	return render(request, 'contact/contact.html', {
		'contact_form': contact_form,
		'site_key': Setting.get_RECAPTCHA_PUBLIC_KEY(),
	})


def get_errors_from_form(form):
	errors = ""
	for k, v in form.errors.items():
		result = re.search('<li>(.*)</li>', str(v))
		errors = errors + result.group(1) + "\n"
		errors = errors.replace('&#39;', "'")
	return errors
