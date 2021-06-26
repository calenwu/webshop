from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from blog.models import ArticlePage, BlogListingPage


@register(BlogListingPage)
class BlogListingTr(TranslationOptions):
	"""
	Country translation fields
	"""
	fields = ['content']


@register(ArticlePage)
class ArticlePageOptions(TranslationOptions):
	"""
	Country translation fields
	"""
	fields = []
