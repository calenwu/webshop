import json
import logging
from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.utils import ProgrammingError

from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import AutoSlugField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image as WagtailImage
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.models import ClusterableModel, ParentalKey, ParentalManyToManyField

from taggit.models import TaggedItemBase

from account.models import User
from blog.forms import ArticlesFilterForm
from streams import blocks


logger = logging.getLogger('django')
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


page_range: int = None
articles_per_page: int = None


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
	def get_ARTICLES_PER_PAGE() -> int:
		"""
		Get the maximum order quantity
		"""
		global articles_per_page
		if articles_per_page is None:
			try:
				articles_per_page = int(Setting.objects.get(key='ARTICLES_PER_PAGE').value)
			except Setting.DoesNotExist:
				return 2
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 2
		return articles_per_page

	@staticmethod
	def get_PAGE_RANGE() -> int:
		"""
		Get the maximum order quantity
		"""
		global page_range
		if page_range is None:
			try:
				page_range = int(Setting.objects.get(key='PAGE_RANGE').value)
			except Setting.DoesNotExist:
				return 2
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 2
		return page_range

	def save(self, *args, **kwargs) -> None:
		super().save(*args, **kwargs)
		if self.key == 'ARTICLES_PER_PAGE':
			global articles_per_page
			articles_per_page = self.value
		elif self.key == 'PAGE_RANGE':
			global page_range
			page_range = self.value


class Tag(TaggedItemBase):
	# cant change name
	content_object = ParentalKey(
		'ArticlePage',
		related_name='blog_tags',
		on_delete=models.CASCADE
	)


class BlogListingPage(RoutablePageMixin, Page):
	"""Listing page lists all the Blog Detail Pages."""
	max_count = 1
	template = 'blog/listing.html'
	subpage_types = ['ArticlePage']
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
		return self.title

	@property
	def link(self):
		return self.url[3:len(self.url)]

	def get_admin_display_title(self):
		return 'Blog Listing Page'

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		context['listing_url'] = self.link
		all_articles = ArticlePage.objects.live().public()
		filter_form = ArticlesFilterForm(initial=request.GET, data=request.GET)
		if filter_form.is_valid():
			try:
				if filter_form.cleaned_data.get('search'):
					searches = json.loads(filter_form.cleaned_data.get('search'))
					if searches:
						for search in searches:
							search = search['value']
							if search.startswith('tag:'):
								search = search[4:].strip()
								all_articles = all_articles.filter(tags__name=search).distinct()
							elif search.startswith('category:'):
								search = search[9:].strip()
								all_articles = all_articles.filter(categories__name=search).distinct()
							elif search.startswith('article:'):
								search = search[8:].strip()
								all_articles = all_articles.filter(title=search).distinct()
							elif search.startswith('author:'):
								search = search[7:].strip().split(' ')
								all_articles = all_articles.filter(
									authors__first_name=search[0], 
									authors__last_name=search[1]).distinct()
							else:
								all_articles = all_articles.filter(title__icontains=search)
			except Exception:
				pass
		paginator = Paginator(all_articles, articles_per_page)
		page = request.GET.get('page')
		previous = []
		next_pages = []
		try:
			articles = paginator.page(page)
		except PageNotAnInteger:
			articles = paginator.page(1)
		except EmptyPage:
			articles = paginator.page(paginator.num_pages)
		for x in articles.paginator.page_range:
			if (articles.number - page_range) <= x < articles.number:
				previous.append(x)
			if (articles.number + page_range) >= x > articles.number:
				next_pages.append(x)
		context['filterForm'] = filter_form
		context['articles'] = articles
		context['empty'] = len(articles) == 0
		context['previous'] = previous
		context['next'] = next_pages
		context['tags'] = request.GET.get('tags', None)
		context['search'] = request.GET.get('search', None)
		return context


class AuthorsOrderable(Orderable):
	""""""
	page = ParentalKey('ArticlePage', related_name='blog_authors')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	unique_together = ('page', 'author')
	panels = [
		SnippetChooserPanel('author')
	]


@register_snippet
class Category(ClusterableModel):
	"""Category for a snippet."""
	name = models.CharField(max_length=255)
	slug = AutoSlugField(populate_from='name', editable=True, unique=True)

	panels = [
		FieldPanel('name'),
		FieldPanel('slug'),
	]

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Blog Categories'
		ordering = ['name']

	def __str__(self):
		return self.name


class CategoriesOrderable(Orderable, Category):
	""""""
	page = ParentalKey('ArticlePage', related_name='blog_categories')


class ArticlePage(RoutablePageMixin, Page):
	"""Blog Article"""
	subpage_types = []
	parent_page_types = [BlogListingPage]
	tags = ClusterTaggableManager(through=Tag, blank=True)
	template = 'blog/details.html'
	subtitle = models.CharField(max_length=255, blank=True, null=True, help_text='Why we love Avicii')
	authors = ParentalManyToManyField(User, blank=False, related_name='blog_authors')
	categories = ParentalManyToManyField(Category, blank=True, related_name='blog_categories')
	preview_image = models.ForeignKey(
		WagtailImage,
		blank=True,
		null=True,
		related_name='+',
		on_delete=models.SET_NULL
	)
	preview_text = models.TextField(blank=True, null=True)
	content = StreamField(
		[
			('richtext', blocks.RichtextBlock()),
			('code', blocks.CodeBlock()),
			('html', blocks.HtmlBlock()),
			('youtube', blocks.YoutubeBlock()),
		], 
		null=True,
		blank=True
	)
	content_panels = Page.content_panels + [
		FieldPanel('subtitle'),
		ImageChooserPanel('preview_image'),
		FieldPanel('preview_text'),
		MultiFieldPanel(
			[
				FieldPanel('authors', widget=forms.CheckboxSelectMultiple)
			], heading=_('Author(s)')
		),
		MultiFieldPanel(
			[
				FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
			], heading=_('Categories')
		),
		FieldPanel('tags'),
		StreamFieldPanel('content')
	]

	@property
	def link(self):
		temp = self.url
		return temp[3:len(temp)]

	@property
	def parent_link(self):
		return self.get_parent().specific.link

	def save(self, *args, **kwargs):
		for lan in settings.LANGUAGES:
			key = make_template_fragment_key('article', [self.id, lan[0]])
			cache.delete(key)
		key = make_template_fragment_key('article', [self.id])
		cache.delete(key)
		return super().save(*args, **kwargs)

	def get_date_readable(self):
		return '{} {} {}'.format(
			self.first_published_at.day,
			MONTH_DICT[self.first_published_at.month],
			self.first_published_at.year)
