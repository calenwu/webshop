import logging
from datetime import datetime
from enum import Enum
from typing import List, Tuple, Dict

from django.core.validators import MinValueValidator
from django.db import models
from django.db.utils import ProgrammingError
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from modelcluster.models import ClusterableModel, ParentalKey

from account.models import User
from coupon.models import Coupon
from home.utils import convert_to_paypal_price, display_currency_price
from shop.models import ProductColorQuantity


logger = logging.getLogger('django')
checkout_timeout: int = None
email_button_color: str = None
email_button_text_color: str = None
invoice_number_prefix = None
invoice_number_start = None
invoice_logo_url: str = None
invoice_company_name: str = None
invoice_company_signature: str = None
invoice_business_id: str = None
invoice_website: str = None
invoice_email: str = None
order_confirmation_subject: str = None
order_number_prefix = None
order_number_start = None
paypal_secret_key: str = None
paypal_client_id: str = None
shipping_confirmation_subject: str = None
stripe_secret_key: str = None
stripe_publishable_key: str = None
tax_percentage: int = None
MONTH_DICT = {
	1: _('January'),
	2: _('February'),
	3: _('March'),
	4: _('April'),
	5: _('May'),
	6: _('June'),
	7: _('July'),
	8: _('August'),
	9: _('September'),
	10: _('October'),
	11: _('November'),
	12: _('December')
}


class Setting(ClusterableModel):
	key = models.CharField(max_length=255, db_index=True, unique=True)
	value = models.CharField(max_length=255, db_index=True, null=True, blank=True)
	image = models.ForeignKey(
		Image,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+',
	)
	panels = [
		FieldPanel('key'),
		FieldPanel('value'),
		ImageChooserPanel('image'),
	]

	class Meta:
		verbose_name = 'Setting'
		verbose_name_plural = 'Settings'
		ordering = ['key']
	
	def __str__(self):
		return self.key

	@staticmethod
	def get_STRIPE_SECRET_KEY() -> str:
		global stripe_secret_key
		if stripe_secret_key is None:
			try:
				stripe_secret_key = Setting.objects.get(key='STRIPE_SECRET_KEY').value
			except Setting.DoesNotExist:
				return 'STRIPE_SECRET_KEY'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'STRIPE_SECRET_KEY'
			except Exception as e:
				logging.error(str(e))
				return 'STRIPE_SECRET_KEY'
		return stripe_secret_key

	@staticmethod
	def get_STRIPE_PUBLISHABLE_KEY() -> str:
		global stripe_publishable_key
		if stripe_publishable_key is None:
			try:
				stripe_publishable_key = Setting.objects.get(key='STRIPE_PUBLISHABLE_KEY').value
			except Setting.DoesNotExist:
				return 'STRIPE_PUBLISHABLE_KEY'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'STRIPE_PUBLISHABLE_KEY'
			except Exception as e:
				return logging.error(str(e))
		return stripe_publishable_key

	@staticmethod
	def get_PAYPAL_SECRET_KEY() -> str:
		global paypal_secret_key
		if paypal_secret_key is None:
			try:
				paypal_secret_key = Setting.objects.get(key='PAYPAL_SECRET_KEY').value
			except Setting.DoesNotExist:
				return 'PAYPAL_SECRET_KEY'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'PAYPAL_SECRET_KEY'
			except Exception as e:
				logging.error(str(e))
				return  'PAYPAL_SECRET_KEY'
		return paypal_secret_key

	@staticmethod
	def get_PAYPAL_CLIENT_ID() -> str:
		global paypal_client_id
		if paypal_client_id is None:
			try:
				paypal_client_id = Setting.objects.get(key='PAYPAL_CLIENT_ID').value
			except Setting.DoesNotExist:
				return 'PAYPAL_CLIENT_ID'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'PAYPAL_CLIENT_ID'
			except Exception as e:
				logging.error(str(e))
				return 'PAYPAL_CLIENT_ID'
		return paypal_client_id

	@staticmethod
	def get_TAX_PERCENTAGE() -> float:
		global tax_percentage
		if tax_percentage is None:
			try:
				tax_percentage = int(Setting.objects.get(key='TAX_PERCENTAGE').value)
			except Setting.DoesNotExist:
				return 20
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 20
			except Exception as e:
				logging.error(str(e))
				return 20
		return tax_percentage

	@staticmethod
	def get_INVOICE_LOGO_URL() -> str:
		"""
		Invoice logo
		"""
		global invoice_logo_url
		if invoice_logo_url is None:
			try:
				invoice_logo_url = Setting.objects.get(key='INVOICE_LOGO').image.file.url
			except Setting.DoesNotExist:
				return 'No logo'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'No logo'
			except Exception as e:
				logging.error(str(e))
				return 'No logo'
		return invoice_logo_url

	@staticmethod
	def get_ORDER_CONFIRMATION_SUBJECT() -> str:
		global order_confirmation_subject
		if order_confirmation_subject is None:
			try:
				order_confirmation_subject = Setting.objects.get(key='ORDER_CONFIRMATION_SUBJECT').value
			except Setting.DoesNotExist:
				return 'Order confirmation'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'Order confirmation'
			except Exception as e:
				logging.error(str(e))
				return 'Order confirmation'
		return order_confirmation_subject

	@staticmethod
	def get_SHIPPING_CONFIRMATION_SUBJECT() -> str:
		global shipping_confirmation_subject
		if shipping_confirmation_subject is None:
			try:
				shipping_confirmation_subject = Setting.objects.get(key='SHIPPING_CONFIRMATION_SUBJECT').value
			except Setting.DoesNotExist:
				return 'Shipping confirmation'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'Shipping confirmation'
			except Exception as e:
				logging.error(str(e))
				return 'Shipping confirmation'
		return shipping_confirmation_subject

	@staticmethod
	def get_ORDER_NUMBER_PREFIX() -> str:
		global order_number_prefix
		if order_number_prefix is None:
			try:
				order_number_prefix = Setting.objects.get(key='ORDER_NUMBER_PREFIX').value
			except Setting.DoesNotExist:
				order_number_prefix = 'ON'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				order_number_prefix = 'ON'
				return 'ON'
			except Exception as e:
				return logging.error(str(e))
		return order_number_prefix

	@staticmethod
	def get_ORDER_NUMBER_START() -> str:
		global order_number_start
		if order_number_start is None:
			try:
				order_number_start = Setting.objects.get(key='ORDER_NUMBER_START').value
			except Setting.DoesNotExist:
				order_number_start = '1000'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				order_number_start = '1000'
				return '1000'
			except Exception as e:
				return logging.error(str(e))
		return order_number_start

	@staticmethod
	def get_INVOICE_NUMBER_PREFIX() -> str:
		global invoice_number_prefix
		if invoice_number_prefix is None:
			try:
				invoice_number_prefix = Setting.objects.get(key='INVOICE_NUMBER_PREFIX').value
			except Setting.DoesNotExist:
				invoice_number_prefix = 'ON'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				invoice_number_prefix = 'ON'
				return 'None'
			except Exception as e:
				return logging.error(str(e))
		return invoice_number_prefix

	@staticmethod
	def get_INVOICE_NUMBER_START() -> str:
		global invoice_number_start
		if invoice_number_start is None:
			try:
				invoice_number_start = Setting.objects.get(key='INVOICE_NUMBER_START').value
			except Setting.DoesNotExist:
				invoice_number_start = '1000'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				invoice_number_start = '1000'
				return '1000'
			except Exception as e:
				return logging.error(str(e))
		return invoice_number_start

	@staticmethod
	def get_INVOICE_COMPANY_NAME() -> str:
		global invoice_company_name
		if invoice_company_name is None:
			try:
				invoice_company_name = Setting.objects.get(key='INVOICE_COMPANY_NAME').value
			except Setting.DoesNotExist:
				return 'INVOICE_COMPANY_NAME'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'INVOICE_COMPANY_NAME'
			except Exception as e:
				return logging.error(str(e))
		return invoice_company_name

	@staticmethod
	def get_INVOICE_COMPANY_SIGNATURE() -> str:
		global invoice_company_signature
		if invoice_company_signature is None:
			try:
				invoice_company_signature = Setting.objects.get(key='INVOICE_COMPANY_SIGNATURE').value
			except Setting.DoesNotExist:
				return 'INVOICE_COMPANY_SIGNATURE'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'INVOICE_COMPANY_SIGNATURE'
			except Exception as e:
				logging.error(str(e))
				return 'INVOICE_COMPANY_SIGNATURE'
		return invoice_company_signature

	@staticmethod
	def get_INVOICE_BUSINESS_ID() -> str:
		global invoice_business_id
		if invoice_business_id is None:
			try:
				invoice_business_id = Setting.objects.get(key='INVOICE_BUSINESS_ID').value
			except Setting.DoesNotExist:
				return 'INVOICE_BUSINESS_ID'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'INVOICE_BUSINESS_ID'
			except Exception as e:
				logging.error(str(e))
				return 'INVOICE_BUSINESS_ID'
		return invoice_business_id

	@staticmethod
	def get_INVOICE_WEBSITE() -> str:
		global invoice_website
		if invoice_website is None:
			try:
				invoice_website = Setting.objects.get(key='INVOICE_WEBSITE').value
			except Setting.DoesNotExist:
				return 'INVOICE_WEBSITE'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'INVOICE_WEBSITE'
			except Exception as e:
				logging.error(str(e))
				return 'INVOICE_WEBSITE'
		return invoice_website

	@staticmethod
	def get_INVOICE_EMAIL() -> str:
		global invoice_email
		if invoice_email is None:
			try:
				invoice_email = Setting.objects.get(key='INVOICE_EMAIL').value
			except Setting.DoesNotExist:
				return 'INVOICE_EMAIL'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'INVOICE_EMAIL'
			except Exception as e:
				logging.error(str(e))
				return 'INVOICE_EMAIL'
		return invoice_email

	@staticmethod
	def get_CHECKOUT_TIMEOUT() -> int:
		"""
		Get how long the user has to check out
		"""
		global checkout_timeout
		if checkout_timeout is None:
			try:
				return int(Setting.objects.get(key='CHECKOUT_TIMEOUT').value)
			except Setting.DoesNotExist:
				return 300
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 300
			except Exception as e:
				logging.error(str(e))
				return 300
		return checkout_timeout

	@staticmethod
	def get_EMAIL_BUTTON_TEXT_COLOR() -> str:
		"""
		Color of the button in the email
		"""
		global email_button_text_color
		if email_button_text_color is None:
			try:
				return Setting.objects.get(key='EMAIL_BUTTON_TEXT_COLOR').value
			except Setting.DoesNotExist:
				return '#ffffff'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return '#ffffff'
			except Exception as e:
				logging.error(str(e))
				return '#ffffff'
		return email_button_text_color

	@staticmethod
	def get_EMAIL_BUTTON_COLOR() -> str:
		"""
		Color of the button in the email
		"""
		global email_button_color
		if email_button_color is None:
			try:
				return Setting.objects.get(key='EMAIL_BUTTON_COLOR').value
			except Setting.DoesNotExist:
				return '#000000'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return '#000000'
			except Exception as e:
				logging.error(str(e))
				return '#000000'
		return email_button_color

	def save(self, *args, **kwargs) -> None:
		super().save(*args, **kwargs)
		if self.key == 'CHECKOUT_TIMEOUT':
			global checkout_timeout
			checkout_timeout = self.value
		elif self.key == 'EMAIL_BUTTON_COLOR':
			global email_button_color
			email_button_color = self.value
		elif self.key == 'EMAIL_BUTTON_TEXT_COLOR':
			global email_button_text_color
			email_button_text_color = self.value
		elif self.key == 'INVOICE_NUMBER_PREFIX':
			global invoice_number_prefix
			invoice_number_prefix = self.value
		elif self.key == 'INVOICE_NUMBER_START':
			global invoice_number_start
			invoice_number_start = self.value
		elif self.key == 'INVOICE_LOGO_URL':
			global invoice_logo_url
			invoice_logo_url = self.value
		elif self.key == 'INVOICE_COMPANY_NAME':
			global invoice_company_name
			invoice_company_name = self.value
		elif self.key == 'INVOICE_BUSINESS_ID':
			global invoice_business_id
			invoice_business_id = self.value
		elif self.key == 'INVOICE_WEBSITE':
			global invoice_website
			invoice_website = self.value
		elif self.key == 'INVOICE_EMAIL':
			global invoice_email
			invoice_email = self.value
		elif self.key == 'ORDER_CONFIRMATION_SUBJECT':
			global order_confirmation_subject
			order_confirmation_subject = self.value
		elif self.key == 'ORDER_NUMBER_PREFIX':
			global order_number_prefix
			order_number_prefix = self.value
		elif self.key == 'ORDER_NUMBER_START':
			global order_number_start
			order_number_start = self.value
		elif self.key == 'PAYPAL_SECRET_KEY':
			global paypal_secret_key
			paypal_secret_key = self.value
		elif self.key == 'PAYPAL_CLIENT_ID':
			global paypal_client_id
			paypal_client_id = self.value
		elif self.key == 'SHIPPING_CONFIRMATION_SUBJECT':
			global shipping_confirmation_subject
			shipping_confirmation_subject = self.value
		elif self.key == 'STRIPE_SECRET_KEY':
			global stripe_secret_key
			stripe_secret_key = self.value
		elif self.key == 'STRIPE_PUBLISHABLE_KEY':
			global stripe_publishable_key
			stripe_publishable_key = self.value
		elif self.key == 'TAX_PERCENTAGE':
			global tax_percentage
			tax_percentage = self.value


@register_snippet
class ShippingMethod(ClusterableModel):
	"""Shipping methods"""
	name = models.CharField(_('Name'), max_length=127)
	description = models.CharField(_('Description'), max_length=127, blank=True, null=True)
	min_weight = models.IntegerField(_('Minimum weight'), default=0, validators=[MinValueValidator(0)])
	max_weight = models.IntegerField(_('Maximum weight'), default=100, validators=[MinValueValidator(0)])
	price = models.IntegerField(_('Price'), validators=[MinValueValidator(0)])
	active = models.BooleanField(_('Active'), default=True)

	panels = [
		FieldPanel('name'),
		FieldPanel('description'),
		FieldPanel('min_weight'),
		FieldPanel('max_weight'),
		FieldPanel('price'),
		FieldPanel('active'),
	]

	class Meta:
		ordering = ('price',)

	def __str__(self):
		return self.name

	def get_full_name(self):
		return '{} ({})'.format(self.name, self.description)

	def get_price(self) -> int:
		return self.price

	def get_display_price(self) -> str:
		return display_currency_price(self.get_price())

	def get_paypal_price(self) -> str:
		return convert_to_paypal_price(self.get_price())


class CountryManager(models.Manager):
	def get_by_natural_key(self, iso_2):
		return self.get(iso_2=iso_2)


class Country(ClusterableModel):
	iso_2 = models.CharField(max_length=2, unique=True)
	iso_3 = models.CharField(max_length=3, unique=True)
	name = models.CharField(max_length=255)
	active = models.BooleanField(default=True)
	order = models.IntegerField(blank=True, null=True)
	objects = CountryManager

	class Meta:
		verbose_name_plural = 'Countries'
		ordering = ('order', 'name', 'iso_2')

	def __str__(self):
		return self.name

	def natural_key(self):
		return (self.iso_2, )

	@staticmethod
	def get_active():
		"""
		Get active countries
		"""
		countries = []
		for country in Country.objects.filter(active=True).order_by('name'):
			countries.append((country.iso_2, country.name))
		return countries


class State(ClusterableModel):
	name = models.CharField(_('name'), max_length=255)
	label = models.CharField(_('label'), max_length=255)
	country = models.ForeignKey(Country, related_name='states', on_delete=models.CASCADE)
	iso = models.CharField(max_length=8)
	state_code = models.CharField(max_length=8)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('name',)

	@staticmethod
	def get_active() -> List[Tuple[str, str]]:
		"""
		Get active countries
		"""
		states = []
		for state in State.objects.filter(active=True):
			states.append((state.iso, state.name))
		return states

	@staticmethod
	def get_dict() -> Dict[str, List[Dict[str, str]]]:
		"""
		Get active countries
		
		Returns
		-------
		dict
			{
				'US': [
					{
						'label': 'State',
						'name': 'Arizona,
						'iso': 'AZ',
					}
				],
				'IT': [
					{
						'label': 'Province',
						'name': 'Milan,
						'iso': 'MA',
					}
				],
			}
		"""
		dic = {}
		for state in State.objects.filter(active=True):
			if state.country.iso_2 not in dic:
				dic[state.country.iso_2] = []
			dic[state.country.iso_2].append(
				{
					'label': state.label,
					'name': state.name,
					'code': state.iso,
				}
			)
		return dic

	def __str__(self):
		return self.name


class OrderStatus(Enum):
	CREATED = _('Created')
	PROCESSING = _('Processing')
	SHIPPED = _('Shipped')
	CANCELED = _('Canceled')
	RETURNED = _('Returned')


class Order(ClusterableModel):
	status = models.CharField(
		choices=[(tag.value, tag.value) for tag in OrderStatus],
		default=OrderStatus.CREATED,
		max_length=63
	)
	paid = models.BooleanField()
	unique_paid_number = models.IntegerField(null=True, blank=True)
	user = models.ForeignKey(User, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
	email = models.EmailField(_('e-mail'), )
	first_name = models.CharField(_('first name'), max_length=63)
	last_name = models.CharField(_('last name'), max_length=63)
	company = models.CharField(_('company'), max_length=127, null=True, blank=True)
	address = models.CharField(_('address'), max_length=127)
	address2 = models.CharField(_('address2'), null=True, blank=True, max_length=127)
	postal_code = models.CharField(_('postal code'), max_length=15)
	country = models.CharField(_('country'), max_length=255)
	city = models.CharField(_('city'), max_length=127)
	state = models.CharField(_('state'), max_length=127, null=True, blank=True)
	telephone = models.CharField(_('telephone'), max_length=127, null=True, blank=True)
	comment = models.TextField(_('comment'), null=True, blank=True)
	shipping_method = models.ForeignKey(
		ShippingMethod,
		related_name="%(app_label)s_%(class)s_related",
		related_query_name="%(app_label)s_%(class)ss",
		on_delete=models.SET_NULL,
		null=True,
		blank=True
	)
	shipping_method_name = models.CharField(_('Shipping method name'), max_length=255)
	shipping_method_price = models.IntegerField(_('Shipping method price'),validators=[MinValueValidator(0)])
	coupon = models.ForeignKey(
		Coupon,
		related_name="%(app_label)s_%(class)s_related",
		related_query_name="%(app_label)s_%(class)ss",
		null=True,
		blank=True,
		on_delete=models.PROTECT
	)
	coupon_name = models.CharField(_('Coupon name'), null=True, blank=True, max_length=255)
	discount = models.IntegerField(_('Discount on order'), default=0, validators=[MinValueValidator(0)])
	url = models.CharField(max_length=31, unique=True)
	stripe_id = models.CharField(null=True, blank=True, max_length=255, unique=True)
	paypal_order_id =  models.CharField(null=True, blank=True, max_length=255, unique=True)
	tracking_number = models.CharField(null=True, blank=True, max_length=255)
	tracking_number_link = models.CharField(null=True, blank=True, max_length=510)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	panels = [
		FieldPanel('user'),
		MultiFieldPanel([
			FieldPanel('email'),
			FieldPanel('first_name'),
			FieldPanel('last_name'),
			FieldPanel('company'),
			FieldPanel('address'),
			FieldPanel('address2'),
			FieldPanel('postal_code'),
			FieldPanel('country'),
			FieldPanel('city'),
			FieldPanel('state'),
			FieldPanel('telephone'),
			FieldPanel('comment'),
		], heading=_('Customer information')),
		SnippetChooserPanel('shipping_method'),
		FieldPanel('shipping_method_name'),
		FieldPanel('shipping_method_price'),
		SnippetChooserPanel('coupon'),
		FieldPanel('coupon_name'),
		FieldPanel('discount'),
		FieldPanel('url'),
		FieldPanel('status'),
		FieldPanel('paid'),
		FieldPanel('tracking_number'),
		FieldPanel('tracking_number_link'),
		MultiFieldPanel([
			FieldPanel('stripe_id'),
			FieldPanel('paypal_order_id'),
		], heading=_('Payment info')),
		InlinePanel('order_items', label='Order items')
	]

	class Meta:
		ordering = ('-created',)

	def __str__(self) -> str:
		return 'Order ' + str(self.id)

	@property
	def order_number(self) -> str:
		return Setting.get_ORDER_NUMBER_PREFIX() + \
				str(int(Setting.get_ORDER_NUMBER_START()) + self.unique_paid_number).zfill(
					len(Setting.get_ORDER_NUMBER_START()))

	@property
	def invoice_number(self)  -> str:
		return Setting.get_INVOICE_NUMBER_PREFIX() + \
				str(int(Setting.get_INVOICE_NUMBER_START()) + self.unique_paid_number).zfill(
					len(Setting.get_INVOICE_NUMBER_START()))

	@staticmethod
	def generate_random_string():
		return get_random_string(length=31)

	@staticmethod
	def generate_unique_paid_number() -> int:
		paid_orders = Order.objects.filter(paid=True).order_by('-unique_paid_number')
		if paid_orders:
			return paid_orders[0].unique_paid_number + 1
		return 0

	def get_country_readable(self) -> str:
		return Country.objects.get(iso_2=self.country).name

	def get_pre_sum(self) -> int:
		return sum(item.get_total_price() for item in OrderItem.objects.filter(order=self))

	def get_display_pre_sum(self) -> str:
		return display_currency_price(self.get_pre_sum())

	def get_total_price(self) -> int:
		total_price = self.get_pre_sum()
		if self.coupon_name:
			total_price -= self.discount
		return int(total_price + self.shipping_method_price)

	def get_display_total_price(self) -> str:
		return display_currency_price(self.get_total_price())

	def get_display_shipping_price(self) -> str:
		return display_currency_price(self.shipping_method_price)

	def get_display_discount(self) -> str:
		return display_currency_price(self.discount)

	def get_pre_tax(self) -> int:
		return int(self.get_total_price() / (1 + (Setting.get_TAX_PERCENTAGE() / 100)))

	def get_display_pre_tax(self) -> str:
		return display_currency_price(self.get_pre_tax())

	def get_tax_amount(self) -> int:
		return self.get_total_price() - self.get_pre_tax()

	def get_display_tax_amount(self) -> str:
		return display_currency_price(self.get_tax_amount())

	def get_discount(self) -> int:
		return self.discount

	def get_display_discount(self) -> str:
		return display_currency_price(self.get_discount())

	def get_date(self) -> datetime.time:
		return self.created.date()

	def get_date_readable(self) -> str:
		return '{}. {}, {}'.format(
			str(self.created.date().day),
			str(MONTH_DICT[self.created.date().month]),
			str(self.created.date().year)
		)

	def get_payment_method(self) -> str:
		if self.stripe_id:
			return 'Credit Card'
		elif self.paypal_order_id:
			return 'Paypal'
		else:
			return 'Not sure'

	def save(self, *args, **kwargs):
		if self.paid and self.unique_paid_number is not None:
			temp = Order.objects.filter(unique_paid_number=self.unique_paid_number)
			if temp:
				if temp.exclude(id=self.id):
					raise UniqueError(_('unique_paid_number has to be unique'))
				if temp[0].id is not self.id:
					raise ValueError(_('Cannot change unique_paid_number once set'))
		if self.paid and self.unique_paid_number is None:
			raise ValueError(_('A paid order has to have a self.unique_paid_number'))
		if not self.paid and self.unique_paid_number is not None:
			raise ValueError(_('An unpaid order cannot have a unique_paid_number'))
		super().save(*args, **kwargs)


class OrderItem(ClusterableModel, Orderable):
	order = ParentalKey(Order, related_name='order_items')
	product_color_quantity = models.ForeignKey(
		ProductColorQuantity,
		related_name='order_items',
		on_delete=models.SET_NULL,
		null=True,
		blank=True
	)
	sku = models.IntegerField()
	name = models.CharField(max_length=255)
	price = models.IntegerField()
	color = models.CharField(max_length=255)
	quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
	size = models.CharField(max_length=63)
	refunded = models.BooleanField(default=False)

	class Meta:
		ordering = ('-order',)

	def __str__(self) -> str:
		return '{}'.format(self.id)

	def get_description(self) -> str:
		return '{} ({} / {})'.format(self.name, self.color, self.size)

	def get_name(self) -> str:
		return self.name

	def get_sku(self) -> int:
		return self.sku

	def get_price(self) -> int:
		return self.price

	def get_display_price(self) -> str:
		return display_currency_price(self.price)

	def get_total_price(self) -> int:
		return self.get_price() * self.quantity

	def get_display_total_price(self) -> str:
		return display_currency_price(self.get_total_price())


class Address(ClusterableModel):
	user = models.ForeignKey(User, related_name='address', on_delete=models.CASCADE)
	first_name = models.CharField(_('first name'), max_length=61)
	last_name = models.CharField(_('last name'), max_length=61)
	company = models.CharField(_('company'), max_length=126, null=True, blank=True)
	email = models.EmailField(_('e-mail'), )
	address = models.CharField(_('address'), max_length=126)
	address2 = models.CharField(_('address2'), null=True, blank=True, max_length=126)
	postal_code = models.CharField(_('postal code'), max_length=15)
	country = models.CharField(_('country'), max_length=255)
	city = models.CharField(_('city'), max_length=125)
	state = models.CharField(_('state'), max_length=125, null=True, blank=True)
	telephone = models.CharField(_('telephone'), max_length=125, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return str(self.user)


class UniqueError(Exception):
	pass
