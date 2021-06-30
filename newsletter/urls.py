from . import views
from django.urls import path
urlpatterns = [
	path('popup/', views.popup, name='popup'),
	path('popup_js/', views.popup_js, name='popup_js'),
	path('subscribe/', views.subscribe, name='subscribe'),
	path('unsubscribe/<encoded_email>/', views.unsubscribe_view, name='unsubscribe'),
]
