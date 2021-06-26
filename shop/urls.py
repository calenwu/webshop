from django.urls import path

from shop import views


urlpatterns = [
	path('tagify_query/', views.tagify_query, name='tagify_query'),
]
