from django.urls import path
from coupon import views


urlpatterns = [
	path('apply/', views.apply, name='apply'),
	path('remove/', views.remove, name='remove'),
]
