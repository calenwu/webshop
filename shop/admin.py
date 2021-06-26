from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from shop.models import (
	ProductCategory,
	ProductColor,
	ProductColorQuantity,
	ProductListingsPage,
	ProductPage,
	ProductSize,
	SizeCategory,
	Setting
)
# Register your models here.


class ProductColorAdmin(admin.ModelAdmin):
	pass


class ProductColorQuantityAdmin(admin.ModelAdmin):
	pass


class SettingsAdmin(ModelAdmin):
	model = Setting
	menu_icon = 'fontawesome icon-store'
	menu_label = _('Shop settings')
	menu_order = 880
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ('key', 'value')
	search_fields = ('key', 'value')


modeladmin_register(SettingsAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductColorQuantity, ProductColorQuantityAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductListingsPage)
admin.site.register(ProductPage)
admin.site.register(ProductSize)
admin.site.register(SizeCategory)
admin.site.register(Setting)
