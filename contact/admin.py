from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from contact.models import Contact, Setting


class SettingsAdmin(ModelAdmin):
	model = Setting
	menu_icon = 'fontawesome icon-envelope-open-text'
	menu_label = _('Contact settings')
	menu_order = 850
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ['key', 'value']
	search_fields = ['key', 'value']


class ContactAdmin(ModelAdmin):
	model = Contact
	menu_icon = 'fontawesome icon-envelope-open-text'
	menu_label = _('Contact')
	menu_order = 800
	add_to_settings_menu = False
	exclude_from_explorer = True
	list_display = ['email', 'message', 'created']
	search_fields = ['email', 'message', 'created']


class ContactDjangoAdmin(admin.ModelAdmin):
	list_display = ['email', 'message', 'created']
	readonly_fields = ['created']
	pass


modeladmin_register(ContactAdmin)
modeladmin_register(SettingsAdmin)
admin.site.register(Contact, ContactDjangoAdmin)
