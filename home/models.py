import logging
from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import ValidationError 
from django.db import models
from django.db.utils import ProgrammingError
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _

from modelcluster.models import ClusterableModel, ParentalKey

from wagtail.admin.edit_handlers import (
	FieldPanel,
	InlinePanel,
	MultiFieldPanel,
	PageChooserPanel,
	StreamFieldPanel
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image as WagtailImage

from streams import blocks


logger = logging.getLogger('django')


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
	def get_GOOGLE_ANALYTICS_MEASUREMENT_ID() -> int:
		"""
		Get the google analytics measurement id
		"""
		try:
			return Setting.objects.get(key='GOOGLE_ANALYTICS_MEASUREMENT_ID').value
		except Setting.DoesNotExist:
			return ''
		except ProgrammingError:
			logging.error(_('Run python manage.py migrate'))
			return ''
		except Exception as e:
			logging.error(str(e))
			return ''
	
	def save(self, *args, **kwargs):
		if self.key == 'GOOGLE_ANALYTICS_MEASUREMENT_ID':
			key = make_template_fragment_key('google_analytics')
			cache.delete(key)
		return super().save(*args, **kwargs)


class HomePage(Page):
	max_count = 1
	templates = 'home/home_page.html'
	parent_page_type = [Page]
	content = StreamField(
		[
			('centered_header', blocks.CenteredHeader()),
			('full_width_carousel', blocks.BannerCarouselBlock()),
			('centered_title_with_text', blocks.CenteredTitleWithText()),
			('image_left_text_right', blocks.ImageLeftTextRight()),
			('image_right_text_left', blocks.ImageRightTextLeft()),
			('hero_block_text_left', blocks.HeroBlockTextLeft()),
			('hero_block_text_right', blocks.HeroBlockTextRight()),
			('hero_product', blocks.HeroProductBlock()),
			('products', blocks.ProductsBlock()),
		], 
		null=True,
		blank=True
	)
	content_panels = Page.content_panels + [
		StreamFieldPanel('content')
	]

	def save(self, *args, **kwargs):
		for lan in settings.LANGUAGES:
			key = make_template_fragment_key('home_page', [lan[0]])
			cache.delete(key)
		key = make_template_fragment_key('home_page')
		cache.delete(key)
		return super().save(*args, **kwargs)


class TextPage(Page):
	templates = 'home/text_page.html'
	parent_page_type = [Page, HomePage]
	body = RichTextField()
	content_panels = Page.content_panels + [
		FieldPanel('body', classname='full'),
	]


class Title(ClusterableModel):
	logo = models.ForeignKey(
		WagtailImage,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)
	text = models.CharField(max_length=127, blank=True, null=True)

	panels = [
		ImageChooserPanel('logo'),
		FieldPanel('text'),
	]

	def __str__(self) -> str:
		if self.text:
			return self.text
		return self.logo.title

	def clean(self):
		# all = Title.objects.all()
		# if all and all[0] is not self:
		# raise ValidationError(_('There already is a title, please edit that one. You can only have 1 title'))
		if self.logo is None and self.text is None:
			raise ValidationError(_('Either logo or text has to be set'))

	def save(self, *args, **kwargs):
		for lan in settings.LANGUAGES:
			key = make_template_fragment_key('title', [lan[0]])
			cache.delete(key)
		key = make_template_fragment_key('title')
		cache.delete(key)
		return super().save(*args, **kwargs)


class InformationBar(ClusterableModel):
	text = models.TextField()
	text_color = models.CharField(max_length=127)
	background_color = models.CharField(max_length=127)
	active = models.BooleanField(default=True)

	def __str__(self) -> str:
		return self.text

	def save(self, *args, **kwargs):
		for lan in settings.LANGUAGES:
			key = make_template_fragment_key('information_bar', [lan[0]])
			cache.delete(key)
		key = make_template_fragment_key('information_bar')
		cache.delete(key)
		return super().save(*args, **kwargs)


class Menu(ClusterableModel):
	"""The navbar menu clusterable model."""
	title = models.CharField(max_length=127)
	slug = AutoSlugField(populate_from='title', editable=True)
	order = models.IntegerField()
	font_awesome_class = models.CharField(
		max_length=63,
		blank=True,
		null=True,
		help_text='fas fa-list; check: https://fontawesome.com/')
	panels = [
		MultiFieldPanel([
			FieldPanel('title'),
			FieldPanel('slug'),
			FieldPanel('order'),
			FieldPanel('font_awesome_class'),
		], heading=_('Menu')),
		InlinePanel('menu_item', label='Menu item')
	]
	
	class Meta: 
		ordering = ['order']

	def __str__(self) -> str:
		return self.title

	def save(self, *args, **kwargs):
		clear_nav_cache()
		return super().save(*args, **kwargs)
	
	def delete(self, *args, **kwargs):
		clear_nav_cache()
		return super().delete(*args, **kwargs)


class MenuItem(ClusterableModel, Orderable):
	menu = ParentalKey(Menu, related_name='menu_item')
	title = models.CharField(max_length=127)
	slug = AutoSlugField(populate_from='title', editable=True, blank=False, null=False)
	link_page = models.ForeignKey(
		Page,
		null=True,
		blank=True,
		on_delete=models.CASCADE,
		related_name='+'
	)
	link_url = models.CharField(max_length=255, blank=True, null=True)
	order = models.IntegerField()
	open_in_new_tab = models.BooleanField(default=False)
	font_awesome_class = models.CharField(
		max_length=63,
		blank=True,
		null=True,
		help_text='fas fa-list; check: https://fontawesome.com/')
	panels = [
		FieldPanel('title'),
		FieldPanel('slug'),
		PageChooserPanel('link_page'),
		FieldPanel('link_url'),
		FieldPanel('order'),
		FieldPanel('open_in_new_tab'),
		FieldPanel('font_awesome_class'),
	]
	
	class Meta: 
		ordering = ['order']

	@property
	def link(self) -> str:
		if self.link_page:
			temp = self.link_page.url
			return temp[3:len(temp)]
		else:
			return self.link_url

	def clean(self):
		if self.link_page is None and self.link_url is None:
			raise ValidationError(_('Either link_page or link_url has to be set'))

	def save(self, *args, **kwargs):
		clear_nav_cache()
		return super().save(*args, **kwargs)
	
	def delete(self, *args, **kwargs):
		clear_nav_cache()
		return super().delete(*args, **kwargs)


class Footer(ClusterableModel):
	"""The footer clusterable model"""
	title = models.CharField(max_length=63)
	slug = AutoSlugField(populate_from='title', editable=True, blank=False, null=False)
	order = models.IntegerField()
	panels = [
		MultiFieldPanel([
			FieldPanel('title'),
			FieldPanel('slug'),
			FieldPanel('order'),
		], heading=_('Footer')),
		InlinePanel('footer_item', label='Footer item')
	]

	class Meta: 
		ordering = ['order']

	def __str__(self) -> str:
		return self.title

	def save(self, *args, **kwargs):
		clear_nav_cache()
		return super().save(*args, **kwargs)
	
	def delete(self, *args, **kwargs):
		clear_nav_cache()
		return super().delete(*args, **kwargs)


class FooterItem(ClusterableModel, Orderable):
	footer = ParentalKey(Footer, related_name='footer_item')
	title = models.CharField(max_length=63)
	slug = AutoSlugField(populate_from='title', editable=True, blank=False, null=False)
	link_page = models.ForeignKey(
		Page,
		null=True,
		blank=True,
		on_delete=models.CASCADE,
		related_name='+'
	)
	link_url = models.CharField(max_length=255, blank=True, null=True)
	open_in_new_tab = models.BooleanField(default=False)
	font_awesome_class = models.CharField(
		max_length=63,
		blank=True,
		null=True,
		help_text='fas fa-list; check: https://fontawesome.com/')
	include_in_mobile_menu = models.BooleanField(default=False)
	panels = [
		FieldPanel('title'),
		PageChooserPanel('link_page'),
		FieldPanel('link_url'),
		FieldPanel('open_in_new_tab'),
		FieldPanel('font_awesome_class'),
		FieldPanel('include_in_mobile_menu'),
	]

	def __str__(self):
		return self.title

	@property
	def link(self) -> str:
		if self.link_page:
			temp = self.link_page.url
			return temp[3:len(temp)]
		else:
			return self.link_url

	def clean(self):
		if self.link_page is None and self.link_url is None:
			raise ValidationError(_('Either link_page or link_url has to be set'))

	def save(self, *args, **kwargs):
		clear_nav_cache()
		return super().save(*args, **kwargs)
	
	def delete(self, *args, **kwargs):
		clear_nav_cache()
		return super().delete(*args, **kwargs)


class FavIcon(ClusterableModel):
	image = models.ForeignKey(
		WagtailImage,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)
	panels = [
		ImageChooserPanel('image'),
	]

	def __str__(self) -> str:
		return self.image.file.name

	def save(self, *args, **kwargs):
		for lan in settings.LANGUAGES:
			key = make_template_fragment_key('favicon', [lan[0]])
			cache.delete(key)
		key = make_template_fragment_key('favicon')
		cache.delete(key)
		return super().save(*args, **kwargs)


def clear_nav_cache() -> None:
	for lan in settings.LANGUAGES:
		key = make_template_fragment_key('navigation', [lan[0]])
		cache.delete(key)
		key = make_template_fragment_key('sub_navs', [lan[0]])
		cache.delete(key)
		key = make_template_fragment_key('nav_tabs', [lan[0]])
		cache.delete(key)
		key = make_template_fragment_key('mobile_nav_tabs', [lan[0]])
		cache.delete(key)
		key = make_template_fragment_key('mobile_nav_footer', [lan[0]])
		cache.delete(key)
		key = make_template_fragment_key('nav_sub_js', [lan[0]])
		cache.delete(key)
		key = make_template_fragment_key('hide_all_tabs', [lan[0]])
		cache.delete(key)
		key = make_template_fragment_key('information_bar', [lan[0]])
		cache.delete(key)
	key = make_template_fragment_key('navigation')
	cache.delete(key)
	key = make_template_fragment_key('sub_navs')
	cache.delete(key)
	key = make_template_fragment_key('nav_tabs')
	cache.delete(key)
	key = make_template_fragment_key('mobile_nav_tabs')
	cache.delete(key)
	key = make_template_fragment_key('mobile_nav_footer')
	cache.delete(key)
	key = make_template_fragment_key('nav_sub_js')
	cache.delete(key)
	key = make_template_fragment_key('hide_all_tabs')
	cache.delete(key)
