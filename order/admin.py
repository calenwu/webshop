import csv
import datetime
from order import paypal

from django.contrib import admin, messages
from django.contrib.admin.options import (
	unquote,
	csrf_protect_m,
	HttpResponseRedirect,
)
from django.db import models
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register


from order.models import Address, Country, Order, OrderItem, OrderStatus, State, ShippingMethod, Setting
from order.tasks import send_invoice, send_shipping_notification
from order.utils import refund_stripe, refund_paypal


class CountryAdmin(ModelAdmin):
	model = Country
	menu_icon = 'fontawesome icon-globe'
	menu_order = 812
	add_to_settings_menu = True
	exclude_from_explorer = True
	list_display = ['name', 'iso_2', 'iso_3', 'active']
	list_filter = ['active']
	search_fields = ['name', 'iso_2', 'iso_3']


class StateAdmin(ModelAdmin):
	model = State
	menu_icon = 'fontawesome icon-globe'  # change as required
	menu_order = 813
	add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
	exclude_from_explorer = True  # or True to exclude pages of this type from Wagtail's explorer view
	list_display = ['name', 'country', 'active']
	list_filter = ['active', 'country']
	search_fields = ['name', 'iso']


class SettingsAdmin(ModelAdmin):
	model = Setting
	menu_icon = 'fontawesome icon-boxes'
	menu_label = _('Order settings')
	menu_order = 870
	add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
	exclude_from_explorer = True  # or True to exclude pages of this type from Wagtail's explorer view
	list_display = ['key', 'value']
	search_fields = ['key', 'value']


class OrderItemAdmin(ModelAdmin):
	model = OrderItem


class OrderAdmin(ModelAdmin):
	model = Order
	menu_icon = 'fontawesome icon-boxes'
	menu_order = 810  # will put in 3rd place (000 being 1st, 100 2nd)
	add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
	exclude_from_explorer = True  # or True to exclude pages of this type from Wagtail's explorer view
	list_display = [
		'id', 'email', 'country', 'created',
	]
	list_filter = ['created', 'updated', 'paid']
	search_fields = ['id', 'order_number', 'email', 'address', 'created']
	inlines = [OrderItemAdmin, ]


class MyButtonHelper(ButtonHelper):
	def add_button(self, classnames_add=None, classnames_exclude=None):
		if classnames_add is None:
			classnames_add = []
		if classnames_exclude is None:
			classnames_exclude = []
		classnames = self.add_button_classnames + classnames_add
		cn = self.finalise_classname(classnames, classnames_exclude)
		return {
			'url': self.url_helper.create_url,
			'label': _('Add %s') % self.verbose_name,
			'classname': cn,
			'title': _('Add a new %s') % self.verbose_name,
		}


def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
	writer = csv.writer(response)

	fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	# write the header row
	writer.writerow([field.verbose_name for field in fields])
	# write data rows
	for obj in queryset:
		data_row = []
		for field in fields:
			value = getattr(obj, field.name)
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value)
		writer.writerow(data_row)
	return response


export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
	return format_html('<a href="{}" target="_blank">View</a>'.format(
		reverse('order:admin_order_detail', args=[obj.id])
	))


def invoice_pdf(obj):
	return format_html('<a href="{}" target="_blank">PDF</a>'.format(reverse('order:invoice_pdf', args=[obj.id])))


class OrderItemDjangoAdmin(admin.StackedInline):
	model = OrderItem


class OrderDjangoAdmin(admin.ModelAdmin):
	change_form_template = 'order/admin/admin_change_form.html'
	actions = [export_to_csv]

	list_display = [
		'id', 'tracking_number', 'tracking_number_link', 'email', 'country',  order_detail, invoice_pdf
	]
	list_editable = ['tracking_number', 'tracking_number_link']
	list_filter = ['paid', 'created', 'updated']
	search_fields = ['id', 'order_number', 'email', 'address']
	readonly_fields = ['created']
	inlines = [OrderItemDjangoAdmin, ]

	def send_invoice(self, request, queryset, celery=False):
		if isinstance(queryset, models.Model):
			obj = queryset
			obj.save()
			if celery:
				send_invoice.delay(obj.id)
			else:
				send_invoice(obj.id)
			self.message_user(request, _('Invoice sent'), messages.SUCCESS)
		else:
			self.message_user(request, _('Invoice could not be sent'), messages.ERROR)

	def send_shipping(self, request, queryset, celery=False):
		if isinstance(queryset, models.Model):
			obj = queryset
			obj.save()
			if celery:
				send_shipping_notification.delay(obj.id)
			else:
				send_shipping_notification(obj.id)
			self.message_user(request, _('Shipping notification sent'), messages.SUCCESS)
		else:
			self.message_user(request, _('Shipping notification could not be sent'), messages.ERROR)

	def refund(self, request, queryset, amount: int):
		if isinstance(queryset, models.Model):
			order = queryset
			order.save()
			if not order.paid or (not order.stripe_id and not order.paypal_order_id) or \
					order.status == OrderStatus.CANCELED or order.status == OrderStatus.RETURNED:
				self.message_user(request, _('Cant refund this order'), messages.ERROR)
			if amount > order.get_total_price():
				self.message_user(request, _('Maximum refund amount: ') + str(order.get_total_price()), messages.ERROR)
			elif amount <= 0:
				self.message_user(request, _('Minimum refund amount: 0'), messages.ERROR)
			else:
				try:
					if order.stripe_id:
						refund_stripe(order.stripe_id, amount)
					else:
						refund_paypal(order.paypal_order_id, amount)
					self.message_user(request, _('Refunded')  + ' ' + str(amount), messages.SUCCESS)
				except Exception as e:
					self.message_user(request, e, messages.ERROR)
		else:
			self.message_user(request, _('Unknown error'), messages.ERROR)

	send_invoice.short_description = _('Send an invoice')
	send_invoice.short_description = _('Send an invoice via celery')

	@csrf_protect_m
	def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
		if request.method == 'POST' and '_view_in_web' in request.POST:
			obj = self.get_object(request, unquote(object_id))
			return HttpResponseRedirect(reverse('order:view', args=[obj.url]))
		elif request.method == 'POST' and '_send_invoice' in request.POST:
			obj = self.get_object(request, unquote(object_id))
			self.send_invoice(request, obj)
			return HttpResponseRedirect(request.get_full_path())
		elif request.method == 'POST' and '_send_invoice_celery' in request.POST:
			obj = self.get_object(request, unquote(object_id))
			self.send_invoice(request, obj, True)
			return HttpResponseRedirect(request.get_full_path())
		elif request.method == 'POST' and '_shipping_notification' in request.POST:
			obj = self.get_object(request, unquote(object_id))
			self.send_shipping(request, obj)
			return HttpResponseRedirect(request.get_full_path())
		elif request.method == 'POST' and '_shipping_notification_celery' in request.POST:
			obj = self.get_object(request, unquote(object_id))
			self.send_shipping(request, obj, True)
			return HttpResponseRedirect(request.get_full_path())
		elif request.method == 'POST' and '_refund' in request.POST:
			if not request.POST['_refund']:
				return HttpResponseRedirect(request.get_full_path())
			obj = self.get_object(request, unquote(object_id))
			try:
				amount = int(request.POST['_refund'])
			except Exception:
				self.message_user(request, _('Please enter a valid number'), messages.ERROR)
				return HttpResponseRedirect(request.get_full_path())
			self.refund(request, obj, amount)
			return HttpResponseRedirect(request.get_full_path())
		return admin.ModelAdmin.changeform_view(
			self,
			request,
			object_id=object_id,
			form_url=form_url,
			extra_context=extra_context,
		)

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		if ('tracking_number' in form.changed_data or 'tracking_number_link' in form.changed_data) and \
				form.cleaned_data['tracking_number'] and form.cleaned_data['tracking_number_link']:
			send_shipping_notification.delay(obj.id)
			order = Order.objects.get(id=obj.id)
			order.status = OrderStatus.SHIPPED
			order.save()


modeladmin_register(CountryAdmin)
modeladmin_register(OrderAdmin)
modeladmin_register(SettingsAdmin)
modeladmin_register(StateAdmin)
admin.site.register(Address)
admin.site.register(Country)
admin.site.register(Order, OrderDjangoAdmin)
admin.site.register(ShippingMethod)
admin.site.register(State)
admin.site.register(Setting)
