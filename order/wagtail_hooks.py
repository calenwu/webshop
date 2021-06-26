from wagtail.core import hooks
from wagtail.admin import widgets as wagtailadmin_widgets

"""
@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
	yield wagtailadmin_widgets.BaseDropdownMenuButton(
		'A page listing button',
		'/goes/to/a/url/',
		priority=10
	)
"""