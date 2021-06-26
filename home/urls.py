from django.urls import path
from . import views


urlpatterns = [
	path('lang_de', views.lang_de, name='lang_de'),
	path('lang_en', views.lang_en, name='lang_en'),
	#path('404', views.page_not_found_error, name='page_not_found_error'),
	#path('500', views.internal_server_error, name='internal_server_error'),
]
