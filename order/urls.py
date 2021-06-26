from django.urls import path
from . import views


urlpatterns = [
	path('', views.information, name='information'),
	path('shipping', views.shipping, name='shipping'),
	path('payment', views.payment, name='payment'),
	path('view/<order_url>', views.view, name='view'),
	path('paypal-webhook/', views.paypal_webhook, name='paypal_webhook'),
	path('paypal-verification/<paypal_order_id>', views.paypal_verification, name='paypal_verification'),
	path('stripe-verification/<payment_intent_id>', views.stripe_verification, name='stripe_verification'),
	path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
	path('admin-order-detail/<order_id>', views.admin_order_detail, name='admin_order_detail'),
	path('invoice-pdf/<order_id>', views.invoice_pdf, name='invoice_pdf'),
	#path('confirmation-email/<order_id>', views.confirmation_email, name='confirmation_email'),
	#path('shipping-email/<order_id>', views.shipping_email, name='shipping_email'),
]
