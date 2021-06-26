from . import views
from django.urls import path
urlpatterns = [
    path('', views.winwheel, name='winwheel'),
    path('js', views.winwheel_js, name='winwheel_js'),
    path('parameters', views.parameters, name='parameters'),
    path('sections', views.sections, name='sections'),
    path('spin', views.spin, name='spin'),
]
