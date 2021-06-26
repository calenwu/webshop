from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from newsletter.models import NewsletterCampaign, Subscriber


class NewsletterCampaignAdmin(ModelAdmin):
	model = NewsletterCampaign
	menu_icon = 'fontawesome icon-newspaper'
	menu_label = _('Newsletter campaign')
	menu_order = 860
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ['title', 'active']


class SubscriberAdminWagtail(ModelAdmin):
	model = Subscriber
	menu_icon = 'fontawesome icon-users'
	menu_label = _('Newsletter subscribers')
	menu_order = 809
	add_to_settings_menu = False
	exclude_from_explorer = True
	list_display = ['email', 'created']
	search_fields = ['email', 'created']


class SubscriberAdmin(admin.ModelAdmin):
	list_display = ['email', 'created']
	readonly_fields = ['encoded_email']


modeladmin_register(NewsletterCampaignAdmin)
modeladmin_register(SubscriberAdminWagtail)
admin.site.register(Subscriber, SubscriberAdmin)
