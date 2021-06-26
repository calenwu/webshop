from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from cart.models import Setting


class SettingsAdmin(ModelAdmin):
	model = Setting
	menu_icon = 'fontawesome icon-shopping-cart'
	menu_label = _('Cart settings')
	menu_order = 840
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ('key', 'value')
	search_fields = ('key', 'value')


modeladmin_register(SettingsAdmin)
admin.site.register(Setting)
