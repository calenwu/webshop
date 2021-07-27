"""Streamfields live in here."""
import logging
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


logger = logging.getLogger('django')


class RichtextBlock(blocks.RichTextBlock):
	"""Richtext with all features."""

	class Meta:
		template = 'streams/richtext_block.html'
		icon = 'doc-full'
		label = _('Richtext')


class HtmlBlock(blocks.RawHTMLBlock):
	"""Html block."""

	class Meta:
		template = 'streams/raw_html_block.html'
		icon = 'code'
		label = _('Html')


class CodeBlock(blocks.StructBlock):
	"""Html block."""
	language = blocks.CharBlock(required=True, help_text=_('Programming language'))
	code = blocks.TextBlock(repuired=True)

	class Meta:
		template = 'streams/code_block.html'
		icon = 'code'
		label = _('Code')


class CardBlock(blocks.StructBlock):
	title = blocks.CharBlock(required=True, help_text=_('Title'))
	cards = blocks.ListBlock(
		blocks.StructBlock(
			[
				('image', ImageChooserBlock(required=True)),
				('title', blocks.CharBlock(required=True, max_length=63)),
				('text', blocks.TextBlock(required=True, max_length=255)),
				('button_page', blocks.PageChooserBlock(required=False)),
				('button_url', blocks.URLBlock(required=False, help_text='Link')),
				('button_text', blocks.CharBlock(required=True, max_length=63)),
			]
		)
	)

	class Meta:
		template = 'streams/card_block.html'
		icon = 'placeholder'
		label = _('Card')


class ReferenceButtonBlock(blocks.StructBlock):
	text = blocks.CharBlock(required=True, help_text=_('Text'))
	url = blocks.URLBlock(required=True, help_text=_('Text'))
	text_color = blocks.CharBlock(required=True, help_text='#ffffff')
	button_bg_color = blocks.CharBlock(required=True, help_text='#ffffff')
	border_color = blocks.CharBlock(required=False, help_text='#ffffff')
	font_awesome_class = blocks.CharBlock(required=False, help_text='fal fa-nice')

	class Meta:
		template = 'streams/reference_button.html'
		icon = 'placeholder'
		label = _('Reference button')


class CenteredTitleWithText(blocks.StructBlock):
	title = blocks.CharBlock(required=True, help_text=_('Title'))
	text = blocks.TextBlock(required=True, help_text=_('Text'))

	class Meta:
		template = 'streams/centered_title_with_text.html'
		icon = 'form'
		label = _('Centered Title with text')


class ImageLeftTextRight(blocks.StructBlock):
	title = blocks.CharBlock(required=True, help_text=_('Title'))
	text = blocks.TextBlock(required=True, help_text=_('Text'))
	image = ImageChooserBlock(required=True, help_text=_('Image'))

	class Meta:
		template = 'streams/image_left_text_right.html'
		icon = 'image'
		label = _('Image left text right')


class ImageRightTextLeft(blocks.StructBlock):
	title = blocks.CharBlock(required=True, help_text=_('Title'))
	text = blocks.TextBlock(required=True, help_text=_('Text'))
	image = ImageChooserBlock(required=True, help_text=_('image'))

	class Meta:
		template = 'streams/image_right_text_left.html'
		icon = 'image'
		label = _('Image right text left')


class HeroBlockTextLeft(blocks.StructBlock):
	image = ImageChooserBlock(required=True, help_text=_('Image'))
	title = blocks.CharBlock(required=True, help_text=_('Title'))
	text = blocks.RichTextBlock(required=True, help_text=_('Text'))
	button_text = blocks.CharBlock(required=False, help_text=_('Button text'))
	button_url = blocks.CharBlock(required=False, help_text=_('Button url'))

	class Meta:
		template = 'streams/hero_block_text_left.html'
		icon = 'form'
		label = _('Hero block text left')


class HeroBlockTextRight(blocks.StructBlock):
	image = ImageChooserBlock(required=True, help_text=_('Image'))
	title = blocks.CharBlock(required=True, help_text=_('Title'))
	text = blocks.RichTextBlock(required=True, help_text=_('Text'))
	button_text = blocks.CharBlock(required=False, help_text=_('Button text'))
	button_url = blocks.CharBlock(required=False, help_text=_('Button url'))

	class Meta:
		template = 'streams/hero_block_text_right.html'
		icon = 'form'
		label = _('Hero block text right')


class CenteredHeader(blocks.StructBlock):
	text = blocks.CharBlock(required=True, help_text=_('Text'))

	class Meta:
		template = 'streams/centered_header.html'
		icon = 'fontawesome icon-heading'
		label = _('Centered Header')


class BannerBlock(blocks.StructBlock):
	image = ImageChooserBlock(required=True, help_text=_('Image'))
	text = blocks.CharBlock(required=True, help_text=_('Title'))
	text_color = blocks.CharBlock(required=True, help_text='#ffffff')

	class Meta:
		template = 'streams/banner_block.html'
		icon = 'form'
		label = _('Banner')


class YoutubeBlock(blocks.StructBlock):
	url = blocks.URLBlock(required=True, help_text=_('Url'))

	class Meta:
		template = 'streams/youtube_block.html'
		icon = 'fontawesome photo-video'
		label = _('Youtube')


class BannerCarouselBlock(blocks.StructBlock):
	slides = blocks.ListBlock(
		blocks.StructBlock(
			[
				('image', ImageChooserBlock(required=True, help_text=_('Image when width is big'))),
				('image_small', ImageChooserBlock(required=True, help_text=_('Image when width is small'))),
				('button_text', blocks.CharBlock(required=False, help_text=_('Button text'))),
				('text_color', blocks.CharBlock(required=False, help_text=_('Button text color'))),
				('button_background_color', blocks.CharBlock(required=False, help_text=_('Button background_color'))),
				('button_border_color', blocks.CharBlock(required=False, help_text=_('Button border color'))),
				('page', blocks.PageChooserBlock(required=False, help_text=_('Page it redirects to on button click'))),
				('url', blocks.CharBlock(required=False, help_text=_('Url it redirects to on button click'))),
			]
		)
	)

	class Meta:
		template = 'streams/banner_carousel_block.html'
		icon = 'fontawesome icon-images'
		label = _('Banner Carousel')

	def get_form_context(self, value, prefix='', errors=None):
		context = super().get_form_context(value, prefix=prefix, errors=errors)
		context['link'] = ['John', 'Paul', 'George', 'Ringo']
		return context

	@property
	def link(self) -> str:
		if self.slides.page:
			temp = self.slides.page.url
			return temp[3:len(temp)]
		else:
			return self.url


class HeroProductBlock(blocks.StructBlock):
	product = blocks.PageChooserBlock(required=True)

	class Meta:
		template = 'streams/hero_product.html'
		icon = 'fontawesome icon-shopping-bag'
		label = _('Hero product')

	def clean(self, value):
		from shop.models import ProductPage
		result = super(HeroProductBlock, self).clean(value)
		errors = {}
		if not ProductPage.objects.filter(id=value['product'].id):
			errors['product'] = ErrorList([
				_('Please select a product page')
			])
			raise ValidationError(_('Please select a product page'), params=errors)
		return result


class ProductsBlock(blocks.StructBlock):
	products = blocks.ListBlock(
		blocks.StructBlock(
			[
				('product', blocks.PageChooserBlock(required=True)),
			]
		)
	)

	class Meta:
		template = 'streams/products.html'
		icon = 'fontawesome icon-shopping-cart'
		label = _('Products')

	def clean(self, value):
		from shop.models import ProductPage
		result = super(ProductsBlock, self).clean(value)
		errors = {}
		for product in value['products']:
			if not ProductPage.objects.filter(id=product['product'].id):
				errors['product'] = ErrorList([
					_('Please only select a product page')
				])
				raise ValidationError(_('Please select a product page'), params=errors)
		return result
