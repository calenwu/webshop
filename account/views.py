import json

from django.contrib import messages
from django.contrib.auth import authenticate, login as login_user, logout as real_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from account.forms import ChangeEmailForm, ChangePasswordForm, UserRegistrationForm
from account.models import User
from account.utils import get_user_from_request

from shop.models import ProductListingsPage

from order.forms import AddressForm, OrderCreateForm
from order.models import State, Order
from order.utils import get_invoice


@csrf_protect
@require_POST
def register(request) -> JsonResponse:
	user_registration_form = UserRegistrationForm(request.POST)
	if user_registration_form.is_valid():
		create_profile(user_registration_form, request)
		return JsonResponse({
			'data': {
				'success': True
			}
		})
	return JsonResponse({
		'data': {
			'success': False, 
			'errors': {
				'email': user_registration_form.errors.get('email', None),
				'password':  user_registration_form.errors.get('password', None),
				'password2':  user_registration_form.errors.get('password2', None),
			}
		}
	})


@csrf_protect 
@require_POST
def login(request) -> JsonResponse:
	user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
	if user is not None:
		login_user(request, user)
		return JsonResponse({
			'data': {
				'success': True
			}
		})
	return JsonResponse({
		'data': {
			'success': False, 
			'error': str(_('Please enter a correct email address and password. Note that both fields may be case-sensitive.'))
		}
	})


def logout(request):
	real_logout(request)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


def create_profile(user_registration_form, request) -> None:
	new_user = user_registration_form.save(commit=False)
	new_user.set_password(user_registration_form.cleaned_data['password'])
	new_user.save()
	new_user = authenticate(username=new_user.email, password=user_registration_form.cleaned_data['password'])
	login_user(request, new_user)


@login_required
def menu(request):
	return render(request, 'account/menu.html')


@login_required
def change_address(request):
	user = get_user_from_request(request)
	addresses = user.address.all()
	form = AddressForm(user.id)
	if addresses:
		form = AddressForm(user.id, instance=addresses[0])
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		updated_request = request.POST.copy()
		updated_request.update({'user': user.id})
		if form.is_valid():
			form = AddressForm(user.id, updated_request)
			if addresses:
				addresses[0].delete()
			form.save()
			messages.success(
				request, 
				json.dumps({
					'data': {
						'title': str(_('Address updated')),
						'innerHTML': str(_('You updated your address successfully')),
						'type': 'success'
					}
				})
			)
	return render(request, 'account/change_address.html', {
		'form': form,
		'states': json.dumps(State.get_dict())
	})


@login_required
def change_email(request):
	user = get_user_from_request(request)
	form = ChangeEmailForm(initial={'email': user.email})
	if request.method == 'POST':
		form = ChangeEmailForm(request.POST)
		if form.is_valid():
			user.email = form.cleaned_data['email']
			user.save()
			messages.success(
				request, 
				json.dumps({
					'data': {
						'title': str(_('Email updated')),
						'innerHTML': str(_('You updated your email successfully')),
						'type': 'success'
					}
				})
			)
	return render(request, 'account/change_email.html', {
		'form': form
	})


@login_required
def change_password(request):
	user = get_user_from_request(request)
	form = ChangePasswordForm()
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			user.set_password(form.cleaned_data['password'])
			user.save()
			messages.success(
				request, 
				json.dumps({
					'data': {
						'title': str(_('Paasword changed')),
						'innerHTML': str(_('You changed your password successfully')),
						'type': 'success'
					}
				})
			)
			login_user(request, user)
	return render(request, 'account/change_password.html', {
		'form': form
	})


@login_required
def orders(request):
	"""
	Orders of a profile view
	"""
	return render(request, 'account/orders.html', {
		'orders': Order.objects.filter(user=request.user, paid=True),
		'products_url': ProductListingsPage.objects.all()[0].link
	})


@login_required
def invoice(request, url):
	"""
	Invoice as html view
	"""
	order = get_object_or_404(Order, paid=True, url=url, user=request.user)
	response = HttpResponse(get_invoice(order), content_type='application/pdf')
	response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.invoice_number)
	return response


def authors(request):
	authors_l = []
	for user in User.objects.filter(is_staff=True):
		authors_l.append(user.first_name + user.last_name)
	return JsonResponse({
		'authors': authors_l
	})
