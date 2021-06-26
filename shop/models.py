import logging
import json

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.utils import ProgrammingError
from django.utils.translation import gettext_lazy as _

from modelcluster.models import ClusterableModel, ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList, \
	StreamFieldPanel
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image as WagtailImage
from wagtail.images.widgets import AdminImageChooser
from wagtail.snippets.models import register_snippet

from django_extensions.db.fields import AutoSlugField

from taggit.models import TaggedItemBase

from home.models import HomePage
from streams import blocks


logger = logging.getLogger('django')
currency: str = None
currency_code: str = None
page_range: int = None
products_per_page:int = None


class Setting(models.Model):
	key = models.CharField(max_length=255, db_index=True, unique=True)
	value = models.CharField(max_length=255, db_index=True)

	class Meta:
		verbose_name = 'Setting'
		verbose_name_plural = 'Settings'
		ordering = ['key']

	def __str__(self):
		return self.key

	@staticmethod
	def get_PRODUCTS_PER_PAGE() -> int:
		"""
		Get the products per page number
		"""
		global products_per_page
		if products_per_page is None:
			try:
				products_per_page = int(Setting.objects.get(key='PRODUCTS_PER_PAGE').value)
			except Setting.DoesNotExist:
				return 3
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 3
			except Exception as e:
				logging.error(str(e))
				return 3
		return products_per_page

	@staticmethod
	def get_PAGE_RANGE() -> int:
		"""
		Get the page range
		"""
		global page_range
		if page_range is None:
			try:
				page_range = int(Setting.objects.get(key='PAGE_RANGE').value)
			except Setting.DoesNotExist:
				return 3
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 3
			except Exception as e:
				logging.error(str(e))
				return e
		return page_range

	@staticmethod
	def get_CURRENCY() -> str:
		"""
		Get the currency
		"""
		global currency
		if currency is None:
			try:
				currency = Setting.objects.get(key='CURRENCY').value
			except Setting.DoesNotExist:
				return '€'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return '€'
			except Exception as e:
				logging.error(str(e))
				return '€'
		return currency

	@staticmethod
	def get_CURRENCY_CODE() -> str:
		"""
		Get the currency
		"""
		global currency_code
		if currency_code is None:
			try:
				currency_code = Setting.objects.get(key='CURRENCY_CODE').value
			except Setting.DoesNotExist:
				return 'EUR'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'EUR'
			except Exception as e:
				return logging.error(str(e))
		return currency_code

	@staticmethod
	def get_CURRENCY_CODE_PAYPAL() -> str:
		"""
		Get the currency code for paypal
		"""
		return Setting.get_CURRENCY_CODE().upper()

	@staticmethod
	def get_CURRENCY_CODE_STRIPE() -> str:
		"""
		Get the currency code for stripe
		"""
		return Setting.get_CURRENCY_CODE().lower()

	def save(self, *args, **kwargs) -> None:
		super().save(*args, **kwargs)
		if self.key == 'PRODUCTS_PER_PAGE':
			global products_per_page
			products_per_page = self.value
		elif self.key == 'PAGE_RANGE':
			global page_range
			page_range = self.value
		elif self.key == 'CURRENCY':
			global currency
			currency = self.value
		elif self.key == 'CURRENCY_CODE':
			global currency_code
			currency_code = self.value


class ProductListingsPage(RoutablePageMixin, Page):
	"""Listing page lists all the Product Detail Pages."""
	max_count = 1
	parent_page_types = [HomePage]
	subpage_types = ['ProductPage']
	template = 'shop/listing.html'
	content = StreamField(
		[
			('banner', blocks.BannerBlock()),
		], 
		null=True,
		blank=True
	)
	content_panels = Page.content_panels + [
		StreamFieldPanel('content')
	]

	def __str__(self):
		return 'Product Listing Page'

	@property
	def link(self):
		return self.url[3:len(self.url)]

	def get_context(self, request, *args, **kwargs):
		"""Adding custom stuff to context"""
		from shop.forms import FilterForm
		page_range = Setting.get_PAGE_RANGE()
		context = super().get_context(request, *args, **kwargs)
		all_products = ProductPage.objects.live().public()
		filter_form = FilterForm(initial=request.GET, data=request.GET)
		if filter_form.is_valid():
			if filter_form.cleaned_data.get('search'):
				try:
					searches = json.loads(filter_form.cleaned_data.get('search'))
					if searches:
						for search in searches:
							search = search['value']
							if search.startswith('product:'):
								search = search[8:].strip()
								all_products = all_products.filter(title=search)
							else:
								all_products = all_products.filter(title__icontains=search)
				except Exception:
					pass
			category = filter_form.cleaned_data.get('category')
			if category:
				all_products = all_products.filter(product_category=category)
		paginator = Paginator(all_products, Setting.get_PRODUCTS_PER_PAGE())
		page = request.GET.get('page')
		previous = []
		next_pages = []
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		for x in products.paginator.page_range:
			if (products.number - page_range) <= x < products.number:
				previous.append(x)
			if (products.number + page_range) >= x > products.number:
				next_pages.append(x)
		context['filterForm'] = filter_form
		context['products'] = products
		context['previous'] = previous
		context['next'] = next_pages
		context['category_filter_choices'] = [('', _('Show all'))] + \
				[(category.slug, category.name) for category in ProductCategory.objects.all()]
		return context


@register_snippet
class ProductCategory(models.Model):
	name = models.CharField(max_length=127, db_index=True, unique=True)
	slug = AutoSlugField(populate_from='name', editable=True)
	image = models.ForeignKey(
		WagtailImage,
		related_name='+',
		on_delete=models.PROTECT
	)
	panels = [
		FieldPanel('name'),
		FieldPanel('slug'),
		ImageChooserPanel('image'),
	]

	class Meta:
		ordering = ['name']
		verbose_name = 'product category'
		verbose_name_plural = 'product categories'

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		temp = super().save(*args, **kwargs)
		for product in self.products.all():
			for lan in settings.LANGUAGES:
				key = make_template_fragment_key('product', [product.id, lan[0]])
				cache.delete(key)
			key = make_template_fragment_key('product', [product.id])
			cache.delete(key)
		return temp


@register_snippet
class SizeCategory(models.Model):
	name = models.CharField(max_length=127, db_index=True, unique=True)
	slug = AutoSlugField(populate_from='name', editable=True)

	panels = [
		FieldPanel('name'),
		FieldPanel('slug'),
	]

	class Meta:
		ordering = ['name']
		verbose_name = 'Product size category'
		verbose_name_plural = 'Product size categories'

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		temp = super().save(*args, **kwargs)
		for product in self.products.all():
			for lan in settings.LANGUAGES:
				key = make_template_fragment_key('product', [product.id, lan[0]])
				cache.delete(key)
			key = make_template_fragment_key('product', [product.id])
			cache.delete(key)
		return temp


@register_snippet
class ProductSize(models.Model):
	name = models.CharField(max_length=31, db_index=True, unique=True)
	slug = AutoSlugField(populate_from='name', editable=True)
	order_sequence = models.IntegerField()
	size_categories = models.ManyToManyField(SizeCategory, related_name='product_sizes')

	panels = [
		FieldPanel('name'),
		FieldPanel('slug'),
		FieldPanel('order_sequence'),
		FieldPanel('size_categories', widget=forms.CheckboxSelectMultiple),
	]

	class Meta:
		ordering = ['order_sequence']
		verbose_name = 'product size'
		verbose_name_plural = 'product sizes'

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		temp = super().save(*args, **kwargs)
		for size_category in self.size_categories.all():
			for product in size_category.products.all():
				for lan in settings.LANGUAGES:
					key = make_template_fragment_key('product', [product.id, lan[0]])
					cache.delete(key)
				key = make_template_fragment_key('product', [product.id])
				cache.delete(key)
		return temp


class Tag(TaggedItemBase):
	content_object = ParentalKey(
		'shop.ProductPage',
		related_name='product_tags',
		on_delete=models.CASCADE
	)


class ProductPageForm(WagtailAdminPageForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# set AdminImageChooser as widgets because for nested inline panels they choose the default widget
		for product_color_forms in self.formsets['product_colors'].forms:
			product_color_forms.formsets['product_color_images'].empty_form.base_fields['image'].widget = AdminImageChooser()
			product_color_forms.formsets['product_color_images'].empty_form.fields['image'].widget = AdminImageChooser()
			product_color_image_forms = product_color_forms.formsets['product_color_images']
			product_color_image_forms.empty_form.fields['image'].widget = AdminImageChooser()
			for form in product_color_image_forms.forms:
				form.base_fields['image'].widget = AdminImageChooser()
				form.fields['image'].widget = AdminImageChooser()

	def clean(self):
		cleaned_data = super().clean()
		return cleaned_data

	def save(self, commit=True):
		page = super().save(commit=False)
		if commit:
			page.save()
		return page


class ProductPage(RoutablePageMixin, Page):
	parent_page_types = [ProductListingsPage]
	subpage_types = []
	template = 'shop/details.html'
	base_form_class = ProductPageForm
	product_category = models.ForeignKey(ProductCategory, related_name='products', db_index=True, on_delete=models.PROTECT)
	size_category = models.ForeignKey(SizeCategory, related_name='products', db_index=True, on_delete=models.PROTECT)
	tags = ClusterTaggableManager(through=Tag, blank=True)
	image = models.ForeignKey(
		WagtailImage,
		null=True,
		blank=False,
		on_delete=models.SET_NULL,
		related_name='+',
	)
	details = RichTextField(null=True, blank=True)
	price = models.IntegerField(
		help_text=_('Use the smallest unit possible (e.g. cents for EUR/USD)'),
		validators=[MinValueValidator(0)])
	sale_price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
	weight = models.IntegerField(
		default=0,
		help_text=_('Use the smallest unit possible (e.g. gram)'),
		validators=[MinValueValidator(0)])
	show_color = models.BooleanField(default=True)
	show_size = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	reference_buttons = StreamField(
		[
			('reference_button', blocks.ReferenceButtonBlock()),
		],
		null=True,
		blank=True
	)
	content = StreamField(
		[
			('centered_title_with_text', blocks.CenteredTitleWithText()),
			('image_left_text_right', blocks.ImageLeftTextRight()),
			('image_right_text_left', blocks.ImageRightTextLeft()),
		],
		null=True,
		blank=True
	)
	content_panels = Page.content_panels + [
		FieldPanel('product_category'),
		FieldPanel('size_category'),
		FieldPanel('tags'),
		ImageChooserPanel('image'),
		FieldPanel('details'),
		FieldPanel('price'),
		FieldPanel('sale_price'),
		FieldPanel('weight'),
		FieldPanel('show_color'),
		FieldPanel('show_size'),
		StreamFieldPanel('reference_buttons'),
		MultiFieldPanel(
			[
				InlinePanel('product_images', label='Image')
			],
			heading=_('Images')
		),
		StreamFieldPanel('content'),
	]
	sidebar_content_panels = [
		MultiFieldPanel( 
			[
				InlinePanel('product_colors', label='Product color', min_num=1)
			],
			heading=_('Product color')
		),
	]
	edit_handler = TabbedInterface([
		ObjectList(content_panels, heading='Content'),
		ObjectList(sidebar_content_panels, heading='Product variations'),
		ObjectList(Page.promote_panels, heading='Promote'),
		ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
	])

	def __str__(self):
		return self.title

	@property
	def aspect_ratio(self):
		return self.image.height / self.image.width

	@property
	def link(self):
		return self.url[3:len(self.url)]

	@property
	def on_sale(self):
		return self.sale_price is not None

	def get_price(self) -> int:
		if self.sale_price:
			return self.sale_price
		return self.price

	def get_display_price(self) -> str:
		return display_currency_price(self.get_price())

	def get_display_price_original(self) -> str:
		return display_currency_price(self.price)

	def get_paypal_price(self) -> str:
		return convert_to_paypal_price(self.get_price())

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		context['product_colors'] = self.product_colors.all()
		return context

	def get_images(self) -> str:
		"""
		Get ProductImage's or ProductPage

		Returns
		-------
		dict
			{
				'images': [{
						src: 'media/image.webp'
						width: '300';
						height: '300';
					}, {
						src: 'media/image.webp',
						width: '300';
						height: '300';
				}],
			}
		"""
		return json.dumps({
			'images': [
					{
						'src': product_image.image.file.url,
						'width': product_image.image.width,
						'height': product_image.image.height
					} for product_image in self.product_images.all()
				]
			})

	def save(self, *args, **kwargs):
		for lan in settings.LANGUAGES:
			key = make_template_fragment_key('product', [self.id, lan[0]])
			cache.delete(key)
		key = make_template_fragment_key('product', [self.id])
		cache.delete(key)
		return super().save(*args, **kwargs)

	"""
	def save(self, *args, **kwargs):
		for product_color in self.product_colors.all():
			print(product_color.product_color_quantity.all())
		super(ProductPage, self).save()
		for product_color in self.product_colors.all():
			print(product_color.product_color_quantity.all())
	"""


class ProductImages(ClusterableModel, Orderable):
	"""Between 1 and 5 images for the home page carousel."""
	page = ParentalKey('shop.ProductPage', related_name='product_images')
	image = models.ForeignKey(
		WagtailImage,
		null=True,
		blank=False,
		on_delete=models.SET_NULL,
		related_name='+',
	)
	description = models.TextField(null=True, blank=True)
	panels = [
		ImageChooserPanel('image'),
		FieldPanel('description'),
	]

	class Meta:
		ordering = ('sort_order',)

	def save(self, *args, **kwargs):
		for lan in settings.LANGUAGES:
			key = make_template_fragment_key('product', [self.page.id, lan[0]])
			cache.delete(key)
		key = make_template_fragment_key('product', [self.page.id])
		cache.delete(key)
		return super().save(*args, **kwargs)


class ProductColor(ClusterableModel, Orderable):
	product = ParentalKey('shop.ProductPage', related_name='product_colors', db_index=True, on_delete=models.CASCADE)
	color = models.CharField(max_length=63, db_index=True)
	slug = AutoSlugField(populate_from=['product', 'color'], editable=True)
	image = models.ForeignKey(
		WagtailImage,
		on_delete=models.CASCADE,
		related_name='+',
	)
	hex = models.CharField(max_length=7)
	hex2 = models.CharField(max_length=7, blank=True, null=True)

	panels = [
		FieldPanel('color'),
		FieldPanel('slug'),
		ImageChooserPanel('image'),
		FieldPanel('hex'),
		FieldPanel('hex2'),
		InlinePanel('product_color_images', label='Image'),
		InlinePanel('product_color_quantities', label='Quantity')
	]

	class Meta:
		unique_together = ('product', 'color',)
		ordering = ('-product_id',)

	def __str__(self):
		return self.product.title + ' ' + self.color

	def save(self, *args, **kwargs):
		created = not self.pk
		temp = super().save(*args, **kwargs)
		if created:
			li = []
			for product_size in self.product.size_category.product_sizes.all():
				x = ProductColorQuantity.objects.create(
						product_color=self,
						product_size=product_size,
						quantity=0
					)
				li.append(x)
				logger.info(x.product_size.name)
			transaction.on_commit(lambda: save_all(li))
			for lan in settings.LANGUAGES:
				key = make_template_fragment_key('product', [self.product.id, lan[0]])
				cache.delete(key)
			key = make_template_fragment_key('product', [self.product.id])
			cache.delete(key)
		return temp

	def get_info(self) -> str:
		"""
		Get information of ProductColor

		Returns
		-------
		dict
			{
				'images': [
					'media/image.webp',
				],
				'quantity': {
					'id': 32
					'size': 'Universal',
					'quantity': 10,
				}
			}
		"""
		info = {
			'images': [{
				'src': self.image.file.url,
				'width': self.image.width,
				'height': self.image.height
			}],
			'quantity': []
		}
		for product_color_image in self.product_color_images.all():
			info['images'].append({
				'src': product_color_image.image.file.url,
				'width': product_color_image.image.width,
				'height': product_color_image.image.height,
			})
		for product_color_quantity in self.product_color_quantities.all():
			info['quantity'].append(
				{
					'id': product_color_quantity.id,
					'size': product_color_quantity.product_size.name,
					'quantity': product_color_quantity.quantity
				}
			)
		return json.dumps(info)


class ProductColorImage(Orderable):
	"""Between 1 and 5 images for the home page carousel."""
	product_color = ParentalKey('shop.ProductColor', related_name='product_color_images')
	image = models.ForeignKey(
		WagtailImage,
		on_delete=models.CASCADE,
		related_name='+',
	)
	description = models.TextField(null=True, blank=True)
	panels = [
		ImageChooserPanel('image'),
		FieldPanel('description'),
	]

	def save(self, *args, **kwargs):
		for lan in settings.LANGUAGES:
			key = make_template_fragment_key('product', [self.product_color.product.id, lan[0]])
			cache.delete(key)
		key = make_template_fragment_key('product', [self.product_color.product.id])
		cache.delete(key)
		return super().save(*args, **kwargs)


class ProductColorQuantity(Orderable, ClusterableModel):
	"""Quantity per product color and size"""
	product_color = ParentalKey('shop.ProductColor', related_name='product_color_quantities')
	product_size = models.ForeignKey(
		ProductSize,
		on_delete=models.PROTECT
	)
	sku = models.CharField(max_length=127, null=True, blank=True)
	quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])

	class Meta:
		unique_together = ('product_color', 'product_size',)

	def __str__(self):
		return str(self.product_color.color) + ' ' + self.product_size.name

	def get_display_variation(self) -> str:
		if self.product_color.product.show_color and self.product_color.product.show_size:
			return self.product_color.color + ' / ' + self.product_size.name
		elif self.product_color.product.show_color:
			return self.product_color.color
		elif self.product_color.product.show_size:
			return self.product_size.name
		else:
			return ''


def two_decimals(s: float) -> str:
	return '%.2f' % s


def display_currency_price(price: int) -> str:
	currency = Setting.get_CURRENCY()
	currency_code = Setting.get_CURRENCY_CODE()
	if currency_code == 'yen':
		return str(currency) + str(price)
	return currency + two_decimals(price / 100)


def convert_to_paypal_price(price: int) -> str:
	currency = Setting.get_CURRENCY()
	if Setting.get_CURRENCY() == 'yen':
		return str(price)
	return str(price / 100).replace(',', '.')


def save_all(li) -> None:
	for x in li:
		x.save()
