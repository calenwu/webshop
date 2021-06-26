import json
import os
import random
from typing import Dict, List

from django.http import JsonResponse
from django.shortcuts import HttpResponse, render
from django.views.decorators.http import require_POST

from newsletter.forms import SubscribeForm
from winwheel.models import WinwheelParameter, WinwheelSection

from webshop.settings.dev import BASE_DIR
from webshop.utils import get_errors_from_form


def winwheel(request):
	subscriber_form = SubscribeForm()
	return render(request, 'winwheel/winwheel.html', {
		'form': subscriber_form,
	})


def winwheel_js(request):
	return render(request, 'winwheel/winwheel_js.html')


def parameters(request):
	winwheel_para = {}
	for para in WinwheelParameter.objects.all():
		winwheel_para[para.label] = para.value
	return JsonResponse(winwheel_para)


def sections(request):
	"""
		returns {
			'data': {
				'text': 'lol',
				'fillStyle': '#ffffff',
				'textFillStyle': '#ffffff',
			}
		}
	"""
	winwheel_sec: List[Dict[str, str]] = []
	for section in WinwheelSection.objects.all():
		winwheel_sec.append({
			'text': section.txt_display_text,
			'fillStyle': section.txt_background_color,
			'textFillStyle': section.txt_color,
		})
	return JsonResponse({'data': winwheel_sec})


@require_POST
def spin(request):
	"""
		returns {
			'data': {
				'displayTitle': 'lol',
				'title': 'lol',
				'text': 'lol',
				'code': 'lol',
			}
		}
	"""
	body_unicode = request.body.decode('utf-8')
	data = json.loads(body_unicode)
	subscriber_form = SubscribeForm(data)
	if subscriber_form.is_valid():
		pool = {}
		index = 0
		for winwheel_section in WinwheelSection.objects.all():
			for x in range(winwheel_section.percentage_of_winning):
				pool[index] = winwheel_section
				index += 1
		winner = pool[random.randint(0, 100)]
		subscriber_form.save()
		return JsonResponse({
			'displayText': winner.txt_display_text,
			'title': winner.txt_result_title,
			'text': winner.txt_result_text,
			'code': winner.coupon.code
		})
	else:
		return JsonResponse({
			'exception': get_errors_from_form(subscriber_form)
		})

