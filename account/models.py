from django.contrib.auth.models import (
	AbstractUser,
	BaseUserManager,
)
from django.db import models
from wagtail.images.models import Image as WagtailImage
from wagtail.snippets.models import register_snippet


class UserManager(BaseUserManager):

	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_staff') is False:
			raise ValueError(
				'Superuser must have is_staff=True.'
			)
		if extra_fields.get('is_superuser') is False:
			raise ValueError(
				'Superuser must have is_superuser=True.'
			)
		return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
	username = None
	email = models.EmailField('email address', unique=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = UserManager()
	# comment profile_picture out when running makemigrations for the first time
	profile_picture = models.ForeignKey(
		WagtailImage,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)

	@property
	def is_employee(self):
		return self.is_active and (
			self.is_superuser
			or self.is_staff
			and self.groups.filter(name='Employees').exists()
		)

	@property
	def is_dispatcher(self):
		return self.is_active and (
			self.is_superuser
			or self.is_staff
			and self.groups.filter(name='Dispatchers').exists()
		)

	def __str__(self):
		return '{} {}'.format(self.first_name, self.last_name)


register_snippet(User)
