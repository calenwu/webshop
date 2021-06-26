from django.urls import path
from . import views


urlpatterns = [
	path('', views.details, name='details'),
	path('add/<int:product_color_quantity_id>/<int:quantity>', views.add, name='add'),
	path('update/<int:product_color_quantity_id>/<int:quantity>', views.update, name='update'),
	path('cart_overlay_content', views.cart_overlay_content, name='cart_overlay_content'),
	path('cart_checkout_top', views.cart_checkout_top, name='cart_checkout_top'),
	path('cart_checkout_right', views.cart_checkout_right, name='cart_checkout_right'),
]
