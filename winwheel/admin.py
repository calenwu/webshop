from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from winwheel.models import WinwheelSection, WinwheelParameter


class WinwheelParameterAdmin(ModelAdmin):
	model = WinwheelParameter
	menu_icon = 'fontawesome icon-trophy'
	menu_label = _('Winwheel parameters')
	menu_order = 890  # starts at 890 for Winwheel app
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ['label', 'value']


class WWinwheelSectionAdmin(ModelAdmin):
	model = WinwheelSection
	menu_icon = 'fontawesome icon-trophy'
	menu_label = _('Winwheel sections')
	menu_order = 891
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ['txt_display_text', 'percentage_of_winning']


class WinwheelParameterDjangoAdmin(admin.ModelAdmin):
	list_display = ['label', 'value']
	list_editable = ['value']
	search_fields = ['label']


class WinwheelSectionDjangoAdmin(admin.ModelAdmin):
	list_display = ['txt_display_text', 'percentage_of_winning']
	list_editable = ['percentage_of_winning']
	search_fields = ['txt_display_text']


admin.site.register(WinwheelSection, WinwheelSectionDjangoAdmin)
admin.site.register(WinwheelParameter, WinwheelParameterDjangoAdmin)
modeladmin_register(WinwheelParameterAdmin)
modeladmin_register(WWinwheelSectionAdmin)
