from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from modelcluster.models import ClusterableModel

from coupon.models import Coupon


class WinwheelSection(ClusterableModel, Orderable):
	txt_display_text = models.CharField(max_length=31, help_text=_('Text on the wheel'))
	txt_result_title = models.CharField(max_length=255, help_text=_('Title after the spin'))
	txt_result_text = models.CharField(max_length=255, help_text=_('Text after the win'))
	txt_color = models.CharField(max_length=255, help_text=_('Text color on the wheel (#ffffff)'))
	txt_background_color = models.CharField(max_length=255, help_text=_('Background color (#ffffff)'))
	percentage_of_winning = models.IntegerField(
		help_text=_('Percentage of it landing on this section (in percent, full number)'),
		validators=[MinValueValidator(1), MaxValueValidator(100)]
	)
	coupon = models.ForeignKey(Coupon, related_name='winwheel_section', null=True, blank=True, on_delete=models.CASCADE)

	panels = [
		FieldPanel('txt_display_text'),
		FieldPanel('txt_result_title'),
		FieldPanel('txt_result_text'),
		FieldPanel('txt_color'),
		FieldPanel('txt_background_color'),
		FieldPanel('percentage_of_winning'),
		SnippetChooserPanel('coupon'),
	]

	def __str__(self):
		return self.txt_display_text


class WinwheelParameter(ClusterableModel, Orderable):
	label = models.CharField(max_length=255)
	value = models.CharField(max_length=255)

	def __str__(self):
		return self.label

	@staticmethod
	def get_WINWHEEL_ACTIVE() -> bool:
		temp = WinwheelParameter.objects.filter(label='WINWHEEL_ACTIVE')
		if temp:
			temp = temp[0].value
			return temp.lower() == 'yes'
		return False

	def save(self, *args, **kwargs):
		for lan in settings.LANGUAGES:
			key = make_template_fragment_key('winwheel', [lan[0]])
			cache.delete(key)
		key = make_template_fragment_key('winwheel')
		cache.delete(key)
		return super().save(*args, **kwargs)
