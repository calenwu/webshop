from django.conf import settings

from django.conf.urls.i18n import is_language_prefix_patterns_used
from django.middleware.locale import LocaleMiddleware

from django.utils import translation

# cookie_language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

class LanguageMiddleware(LocaleMiddleware):
	def process_request(self, request):
		urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
		language = translation.get_language_from_request(request, check_path=is_language_prefix_patterns_used(urlconf))
		language_from_path = translation.get_language_from_path(request.path_info)
		if language_from_path is not None:
			language = language_from_path
		translation.activate(language)
		request.LANGUAGE_CODE = language
