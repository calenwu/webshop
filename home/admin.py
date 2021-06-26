from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from home.models import FavIcon, Footer, HomePage, InformationBar, Menu, TextPage, Title


class FavIconAdmin(ModelAdmin):
	model = FavIcon
	menu_icon = 'fontawesome icon-image'
	menu_label = _('Favicon')
	menu_order = 810
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ['image',]


class FooterAdmin(ModelAdmin):
	model = Footer
	menu_icon = 'fontawesome icon-list-ul'
	menu_label = _('Footer')
	menu_order = 702
	add_to_settings_menu = False
	exclude_from_explorer = True
	list_display = ['title', 'slug', 'order']
	search_fields = ['title', 'slug', 'order']


class TitleAdmin(ModelAdmin):
	model = Title
	menu_icon = 'fontawesome icon-heading'
	menu_label = _('Title')
	menu_order = 811
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ['text',]
	search_fields = ['text',]


class MenuAdmin(ModelAdmin):
	model = Menu
	menu_icon = 'fontawesome icon-list-ol'
	menu_label = _('Menu')
	menu_order = 701
	add_to_settings_menu = False
	exclude_from_explorer = True
	list_display = ['title', 'slug', 'order']
	search_fields = ['title', 'slug', 'order']


class InformationBarAdmin(ModelAdmin):
	model = InformationBar
	menu_icon = 'fontawesome icon-bells'
	menu_label = _('Information bar')
	menu_order = 812
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ['text', 'active']
	search_fields = ['text', 'active']


modeladmin_register(FavIconAdmin)
modeladmin_register(FooterAdmin)
modeladmin_register(InformationBarAdmin)
modeladmin_register(MenuAdmin)
modeladmin_register(TitleAdmin)
admin.site.register(FavIcon)
admin.site.register(Footer)
admin.site.register(HomePage)
admin.site.register(InformationBar)
admin.site.register(Menu)
admin.site.register(TextPage)
admin.site.register(Title)
