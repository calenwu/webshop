from django import template
from winwheel.models import WinwheelParameter


register = template.Library()


@register.simple_tag()
def get_winwheel_active() -> bool:
	return WinwheelParameter.get_WINWHEEL_ACTIVE()
