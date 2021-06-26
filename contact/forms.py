import logging
from smtplib import SMTPAuthenticationError

from django import forms
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from contact.models import Contact
from webshop.settings import base


logger = logging.getLogger('django')


class ContactForm(forms.ModelForm):
	name = forms.CharField(
		label=_('Name'),
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Name')
			}
		),
	)
	email = forms.EmailField(
		label=_('Email'),
		widget=forms.TextInput(
			attrs={
				"type": "email",
				'placeholder': 'email@gmail.com'
			}
		),
	)
	message = forms.CharField(
		label=_('Message'),
		widget=forms.Textarea(
			attrs={
				'placeholder': 'Message'
			}
		),
	)

	class Meta:
		model = Contact
		fields = ('name', 'email', 'message', )

	def save(self, commit=True):
		instance = super(ContactForm, self).save(commit=False)
		try:
			send_mail(
				str(_('New message from webshop')),
				f'{instance.email} wrote: {instance.message}',
				base.EMAIL_HOST_USER,
				[base.EMAIL_HOST_USER],
				fail_silently=False,
			)
		except SMTPAuthenticationError as e:
			logger.error(_('New contact: ' + str(e)))
		if commit:
			instance.save()
