from modeltranslation.translator import translator, TranslationOptions
from newsletter.models import NewsletterCampaign


class NewsletterCampaignOptions(TranslationOptions):
	"""
	Country translation fields
	"""
	fields = ['title', 'text_done', 'title_done', 'text_done']


translator.register(NewsletterCampaign, NewsletterCampaignOptions)
