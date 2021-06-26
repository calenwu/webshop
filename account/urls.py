from django.contrib.auth import views as auth_views
from django.urls import path

from account import views
from account.forms import CustomPasswordResetForm


urlpatterns = [
	path('address', views.change_address, name='change_address'),
	path('authors', views.authors, name='authors'),
	path('email', views.change_email, name='change_email'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('menu', views.menu, name='menu'),
	path('orders', views.orders, name='orders'),
	path('orders/<url>', views.invoice, name='invoice'),
	path('password', views.change_password, name='change_password'),
	path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('register/', views.register, name='register'),
	path('reset/', 
		auth_views.PasswordResetView.as_view(
			form_class=CustomPasswordResetForm,
			success_url='/'
		),
		name='reset',
	),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
