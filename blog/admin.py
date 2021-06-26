from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from blog.models import ArticlePage, BlogListingPage, Category, Setting, Tag


class SettingsAdmin(ModelAdmin):
	model = Setting
	menu_icon = 'fontawesome icon-newspaper'  # change as required
	menu_label = _('Blog settings')
	menu_order = 830
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ('key', 'value')
	search_fields = ('key', 'value')


modeladmin_register(SettingsAdmin)
admin.site.register(ArticlePage)
admin.site.register(BlogListingPage)
admin.site.register(Category)
admin.site.register(Setting)
admin.site.register(Tag)
