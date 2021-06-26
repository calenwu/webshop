from django.urls import path

from blog import views


urlpatterns = [
	path('tagify_query/', views.tagify_query, name='tagify_query'),
]
