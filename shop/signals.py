import logging
from django.db import transaction
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from shop.models import ProductSize, ProductPage, ProductColor, ProductColorQuantity 


logger = logging.getLogger('django')


'''
# , uid='create_product_color_quantities'
@receiver(post_save, sender=ProductColor)
def create_product_color_quantities(sender, instance, **kwargs) -> None:
	li = []
	if kwargs.get('created', True):
		for product_size in instance.product.size_category.product_sizes.all():
			x = ProductColorQuantity.objects.create(
					product_color=instance,
					product_size=product_size,
					quantity=0
				)
			li.append(x)
	transaction.on_commit(lambda: save_all(li))
	def save_all(li) -> None:
		for x in li:
			x.save()

'''

# , uid='create_product_quantity_for_new_size'
@receiver(m2m_changed, sender=ProductSize.size_categories.through)
def create_product_quantity_for_new_size(sender, instance, **kwargs) -> None:
	action = kwargs.pop('action', None)
	if action == 'post_add':
		logger.info(
			'Create new ProductQuantity for each ProductColor with the new ProductSize: ' +
			str(instance.id))
		for size_category in instance.size_categories.all():
			for product in ProductPage.objects.filter(size_category=size_category):
				for product_color in product.product_colors.all():
					x = ProductColorQuantity.objects.create(
						product_color=product_color,
						product_size=instance,
						quantity=0,
					)
					x.save()

