import logging
from django.db import models
from django.db.utils import ProgrammingError
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger('django')
maximum_order_quantity: int = None
save_abandoned_cart: int = None


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
	def get_MAXIMUM_ORDER_QUANTITY() -> int:
		"""
		Get the maximum order quantity
		"""
		global maximum_order_quantity
		if maximum_order_quantity is None:
			try:
				maximum_order_quantity = int(Setting.objects.get(key='MAXIMUM_ORDER_QUANTITY').value)
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return True
			except Setting.DoesNotExist:
				return 20
			except Exception as e:
				logging.error(str(e))
				return 20
		return maximum_order_quantity

	@staticmethod
	def get_SAVE_ABANDONED_CART() -> bool:
		"""
		Get the maximum order quantity
		"""
		global save_abandoned_cart
		if save_abandoned_cart is None:
			try:
				save_abandoned_cart = Setting.objects.get(key='SAVE_ABANDONED_CART').value.lower() == 'yes'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return True
			except Setting.DoesNotExist:
				return True
			except Exception as e:
				logging.error(str(e))
				return True
		return save_abandoned_cart

	def save(self, *args, **kwargs) -> None:
		super().save(*args, **kwargs)
		if self.key == 'MAXIMUM_ORDER_QUANTITY':
			global maximum_order_quantity
			maximum_order_quantity = self.value
		elif self.key == 'SAVE_ABANDONED_CART':
			global save_abandoned_cart
			save_abandoned_cart = self.value
