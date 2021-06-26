from enum import Enum
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from wagtail.snippets.models import register_snippet

from home.utils import display_currency_price


class CouponType(Enum):
	CREDIT = 'Credit'
	PERCENTAGE = 'Percentage'


# doesnt matter, just so it works for SnippetChooserPanel
@register_snippet
class Coupon(models.Model):
	code = models.CharField(max_length=50, unique=True)
	coupon_type = models.CharField(
		choices=[(tag.value, tag.value) for tag in CouponType],
		default=CouponType.PERCENTAGE,
		max_length=63
	)
	percentage = models.IntegerField(
		_('Percentage'),
		default=0,
		validators=[MinValueValidator(0), MaxValueValidator(100)]
	)
	credit_value = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	credit_used = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	one_time = models.BooleanField(default=False)
	valid_from = models.DateTimeField(default=timezone.now)
	valid_to = models.DateTimeField(default=timezone.now)
	active = models.BooleanField(default=True)

	def __str__(self) -> str:
		return self.code

	@property
	def credit_left(self):
		return self.credit_value - self.credit_used

	def get_full_name(self) -> str:
		if self.coupon_type == CouponType.CREDIT.value:
			return '{} ({})'.format(self.code, self.display_credit_value())
		else:
			return '{} ({}%)'.format(self.code, self.percentage)

	def is_valid(self) -> bool:
		"""
		Check if coupon is valid
		"""
		if self.coupon_type == CouponType.CREDIT.value and self.credit_value == 0:
			return False
		if not self.active:
			return False
		if timezone.now() > self.valid_to or timezone.now() < self.valid_from:
			return False
		return True

	def display_percentage(self):
		return str(self.percentage) + '%'

	def display_credit_value(self):
		return display_currency_price(self.credit_value)
