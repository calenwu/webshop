from django import forms
from django.utils.translation import gettext_lazy as _
from newsletter.models import Subscriber


class SubscribeForm(forms.ModelForm):
	email = forms.CharField(
		label=_('Email'), 
		widget=forms.TextInput(
			attrs={
				'type': 'text',
				'placeholder': 'email@gmail.com'
			}
		)
	)

	class Meta:
		model = Subscriber
		fields = ('email', )
