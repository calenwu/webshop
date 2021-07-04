import urllib
from django import template
from django.conf import settings
from typing import List
from home.models import FavIcon, Footer, FooterItem, InformationBar, Menu, Setting, Title


register = template.Library()


@register.simple_tag()
def get_menu(slug) -> List[Menu]:
	return Menu.objects.get(slug=slug)


@register.simple_tag()
def get_all_menu() -> List[Menu]:
	return Menu.objects.all()


@register.simple_tag()
def get_all_footer() -> List[Footer]:
	return Footer.objects.all()


@register.simple_tag()
def get_footer() -> List[FooterItem]:
	return FooterItem.objects.all()


@register.simple_tag()
def get_footer_mobile() -> List[FooterItem]:
	return FooterItem.objects.filter(include_in_mobile_menu=True)


@register.simple_tag()
def get_title() -> str:
	return Title.objects.all()[0]


@register.simple_tag()
def get_domain() -> str:
	return settings.BASE_URL


@register.simple_tag()
def get_information_bar() -> InformationBar:
	temp = InformationBar.objects.filter(active=True)
	if temp:
		return temp[0]
	return None


@register.simple_tag()
def get_favicon() -> str:
	temp = FavIcon.objects.all()
	if temp:
		return temp[0].image.file.url
	return None


@register.simple_tag()
def change_page(url, page) -> str:
	url_parsed = urllib.parse.urlparse(url)
	parameters = urllib.parse.parse_qs(url_parsed.query)
	parameters['page'] = page
	temp = urllib.parse.urlencode(parameters)
	return url_parsed.path + '?' + temp.replace('%27%5B', '').replace('%27%5D', '')


@register.simple_tag()
def get_google_analytics_measurement_id() -> str:
	return Setting.get_GOOGLE_ANALYTICS_MEASUREMENT_ID()
