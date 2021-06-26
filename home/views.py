import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation

from home.models import HomePage


def home(request):
	return HomePage.objects.live()[0].serve(request)


def lang_de(request):
	language = 'de'
	translation.activate(language)
	request.session[translation.LANGUAGE_SESSION_KEY] = language
	response = HttpResponseRedirect(re.sub('/../', '/de/', request.META.get('HTTP_REFERER', '/')))
	response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
	return response


def lang_en(request):
	language = 'en'
	translation.activate(language)
	request.session[translation.LANGUAGE_SESSION_KEY] = language
	response = HttpResponseRedirect(re.sub('/../', '/en/', request.META.get('HTTP_REFERER', '/')))
	response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
	return response


def page_not_found_error(request):
	return render(request, '404.html')


def internal_server_error(request):
	return render(request, '500.html')