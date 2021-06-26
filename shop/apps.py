from django.apps import AppConfig
from django.db.models.signals import post_save


class ShopConfig(AppConfig):
	name = 'shop'

	def ready(self):
		from shop.models import ProductSize
		from shop.signals import create_product_quantity_for_new_size
		post_save.connect(create_product_quantity_for_new_size, sender=ProductSize)

