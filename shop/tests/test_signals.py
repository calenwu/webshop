from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from home.models import HomePage

from shop.models import ProductCategory, SizeCategory, ProductSize, ProductPage, ProductImages, ProductColor, \
	ProductColorImage, ProductColorQuantity
from shop.tests.utilities import create_wagtail_image

from webshop.settings.dev import BASE_DIR

from wagtail.core.models import Page
from wagtail.images.models import Image


image_path = BASE_DIR + '/shop/static/shop/img/test/test.webp'
file_mock = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')


class SignalsTestCase(TestCase):
	product: ProductPage = None

	def setUp(self):
		root_page = Page.get_root_nodes()[0]
		home_page = HomePage(title='Home Page', title_en='Home Page')
		root_page.add_child(instance=home_page)
		root_page.title = 'Root Page'
		root_page.title_en = 'Root Page'
		root_page.save()
		home_page.save()

	def test_create_product_color_quantities_after_new_product_color(self):
		pass

	def test_create_product_color_quantities_after_new_product_size(self):
		pass
