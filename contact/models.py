import logging
from django.db import models
from django.db.utils import ProgrammingError
from django.utils.translation import gettext_lazy as _

from wagtail.core.models import Orderable

from modelcluster.models import ClusterableModel


logger = logging.getLogger('django')
recaptcha_public_key: str = None
recaptcha_private_key: str = None

class Setting(ClusterableModel, Orderable):
	key = models.CharField(max_length=255, db_index=True, unique=True)
	value = models.CharField(max_length=255, db_index=True)

	class Meta:
		verbose_name = 'Setting'
		verbose_name_plural = 'Settings'
		ordering = ['key']

	def __str__(self):
		return self.key

	@staticmethod
	def get_RECAPTCHA_PUBLIC_KEY() -> str:
		"""
		Get the maximum order quantity
		"""
		global recaptcha_public_key
		if recaptcha_public_key is None:
			try:
				recaptcha_public_key = Setting.objects.get(key='RECAPTCHA_PUBLIC_KEY').value
			except Setting.DoesNotExist:
				return 'None'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'None'
			except Exception as e:
				return logging.error(str(e))
		return recaptcha_public_key

	@staticmethod
	def get_RECAPTCHA_PRIVATE_KEY() -> str:
		"""
		Get the maximum order quantity
		"""
		global recaptcha_private_key
		if recaptcha_private_key is None:
			try:
				recaptcha_private_key = Setting.objects.get(key='RECAPTCHA_PRIVATE_KEY').value
			except Setting.DoesNotExist:
				return 'None'
			except ProgrammingError:
				logging.error(_('Run python manage.py migrate'))
				return 'None'
			except Exception as e:
				return logging.error(str(e))
		return recaptcha_private_key

	def save(self, *args, **kwargs) -> None:
		super().save(*args, **kwargs)
		if self.key == 'RECAPTCHA_PUBLIC_KEY':
			global recaptcha_public_key
			recaptcha_public_key = self.value
		elif self.key == 'RECAPTCHA_PRIVATE_KEY':
			global recaptcha_private_key
			recaptcha_private_key = self.value


class Contact(ClusterableModel, Orderable):
	name = models.CharField(max_length=80)
	email = models.EmailField()
	message = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('created', )

	def __str__(self):
		return self.email
