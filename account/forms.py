import logging
from django import forms
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
	UserCreationForm as DjangoUserCreationForm
)
from django.contrib.auth.forms import UsernameField, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from wagtail.images.models import Image
from wagtail.images.widgets import AdminImageChooser
from wagtail.users.forms import (
	UserEditForm,
)

from account import models

logger = logging.getLogger('django')


class AuthenticationForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(
		strip=False, widget=forms.PasswordInput
	)

	def __init__(self, request=None, *args, **kwargs):
		self.request = request
		self.user = None
		super().__init__(*args, **kwargs)

	def clean(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		if email is not None and password:
			self.user = authenticate(
				self.request, email=email, password=password
			)
			if self.user is None:
				raise forms.ValidationError(
					'Invalid email/password combination'
				)
			logger.info('Authentication successful for email=%s', email)

	def get_user(self):
		return self.user


class UserCreationForm(DjangoUserCreationForm):

	class Meta(DjangoUserCreationForm.Meta):
		model = models.User
		fields = ('email',)
		field_classes = {'email': UsernameField}

	def send_mail(self):
		logger.info(
			'Sending signup email for email=%s',
			self.cleaned_data['email'],
		)
		message = 'Welcome{}'.format(self.cleaned_data['email'])
		send_mail(
			'Welcome to BookTime',
			message,
			'support@kalunagoods.com',
			[self.cleaned_data['email']],
			fail_silently=True,
		)


class CustomUserCreationForm(UserCreationForm):
	profile_picture = forms.ImageField(widget=AdminImageChooser(), required=False)


class CustomUserEditForm(UserEditForm):
	profile_picture = forms.ModelChoiceField(
		queryset=Image.objects.all(),
		widget=AdminImageChooser(),
		required=False
	)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		instance = kwargs.get('instance', None)
		if instance and instance.profile_picture:
			self.fields['profile_picture'].initial = instance.profile_picture.pk

	def save(self, commit=True):
		user: models.User
		user = super().save(self)
		user.profile_picture = self.cleaned_data['profile_picture']
		user.save()
		return user


class UserRegistrationForm(forms.ModelForm):
	email = forms.EmailField()
	password = forms.CharField(max_length=63)
	password2 = forms.CharField()

	class Meta:
		model = models.User
		fields = ('email',)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if models.User.objects.filter(email=email).exists():
			raise forms.ValidationError('This email is already in use')
		return email

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Passwords don\'t match.')
		return cd['password2']

	def clean(self):
		return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
	"""
	Overriding the Email Password Reset Forms Save to be able to send HTML email
	"""
	def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
			use_https=False, token_generator=default_token_generator, request=None,
			email_subject_name='registration/password_reset_subject.txt', **kwargs):
		"""
		Generate a one-use only link for resetting password and send it to the
		user.
		"""
		email = self.cleaned_data['email']
		for user in self.get_users(email):
			site_name = domain = domain_override
			context = {
				'email': email,
				'domain': domain,
				'site_name': site_name,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'user': user,
				'token': token_generator.make_token(user),
				'protocol': 'https' if use_https else 'http',
			}
			render = render_to_string(email_template_name, context)
			render_subject = str(_('Reset password'))
			msg = EmailMultiAlternatives(render_subject, strip_tags(render), None, [user.email])
			msg.attach_alternative(render, 'text/html')
			msg.send()


class ChangeEmailForm(forms.Form):
	email = forms.EmailField(
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Email'),
			}
		)
	)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if models.User.objects.filter(email=email).exists():
			raise forms.ValidationError('This email is already in use')
		return email

	def clean(self):
		return self.cleaned_data


class ChangePasswordForm(forms.Form):
	password = forms.CharField(
		max_length=63,
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Email'),
			}
		)
	)
	password2 = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Email'),
			}
		)
	)

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Passwords don\'t match.')
		return cd['password2']

	def clean(self):
		return self.cleaned_data
