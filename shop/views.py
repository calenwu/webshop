from django.http import JsonResponse
from shop.models import ProductPage


def tagify_query(request):
	all_products = ProductPage.objects.live().public()
	tags = list(dict.fromkeys(all_products.values_list('tags__name', flat=True)))
	products = list(ProductPage.objects.live().public().values_list('title', flat=True))
	return JsonResponse({
		'products': products,
		'tags': tags,
	})
