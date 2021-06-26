from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from coupon.models import Coupon


class CouponAdmin(ModelAdmin):
	model = Coupon
	menu_icon = 'fontawesome icon-percent'
	menu_order = 801
	add_to_settings_menu = False
	exclude_from_explorer = True
	list_display = ['code', 'coupon_type', 'active']
	list_filter = ['coupon_type', 'active']
	search_fields = ['code', 'coupon_type']


modeladmin_register(CouponAdmin)
admin.site.register(Coupon)
