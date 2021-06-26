from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image as WagtailImage

from modelcluster.models import ClusterableModel

from webshop.utils import encode, decode

SECRET_KEY = 'ABCDABCDABCDABCDABCDABCDABCD'


class NewsletterCampaign(ClusterableModel):
	title = models.TextField()
	image = models.ForeignKey(
		WagtailImage,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)
	text = models.TextField()
	title_done = models.TextField(help_text=_('Title for the popup after subscribing'))
	text_done = models.TextField(help_text=_('Text for the popup after subscribing'))
	active = models.BooleanField(default=True)

	panels = [
		FieldPanel('title'),
		ImageChooserPanel('image'),
		FieldPanel('text'),
		FieldPanel('title_done'),
		FieldPanel('text_done'),
		FieldPanel('active'),
	]

	class Meta:
		verbose_name = _('Newsletter campaign')
		verbose_name_plural = _('Newsletter campaigns')

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		for lan in settings.LANGUAGES:
			key = make_template_fragment_key('newsletter_popup_js', [lan[0]])
			cache.delete(key)
		key = make_template_fragment_key('newsletter_popup_js')
		cache.delete(key)
		return super().save(*args, **kwargs)


class Subscriber(ClusterableModel):
	email = models.EmailField(unique=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('Subscriber')
		verbose_name_plural = _('Subscribers')
		ordering = ('created', 'email')

	def __str__(self):
		return self.email

	@property
	def encoded_email(self):
		return encode(SECRET_KEY, self.email)

	@staticmethod
	def decode_email(encoded_mail):
		return decode(SECRET_KEY, encoded_mail)

	@staticmethod
	def is_encoded_email_valid(encoded_email):
		"""
		If encoded email is valid
		"""
		subscriber = Subscriber.objects.filter(email=decode(SECRET_KEY, encoded_email))
		return len(subscriber) != 0
