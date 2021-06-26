from typing import List

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from wagtail.images.models import Image
from webshop.settings.dev import BASE_DIR

from account.models import User
from home.models import HomePage
from shop.models import ProductListingsPage, ProductCategory, SizeCategory, ProductSize


def get_driver() -> webdriver.Chrome:
	chrome_driver = settings.BASE_DIR + '/chromedriver'
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-setuid-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--window-position=0,0')
	chrome_options.add_argument('--ignore-certifcate-errors')
	chrome_options.add_argument('--ignore-certifcate-errors-spki-list')
	chrome_options.add_argument('--window-size=1920x1080')
	chrome_options.add_argument(
		'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
	chrome_options.add_argument('sec-fetch-mode=cors')
	chrome_options.add_argument('accept-language=en-US,en;q=0.9')
	chrome_options.add_argument('authorization=')
	chrome_options.add_argument('x-requested-with=XMLHttpRequest')
	chrome_options.add_argument('appos=web')
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
	driver.implicitly_wait(10)
	return driver


def login(driver: webdriver.Chrome, server_url: str):
	if not User.objects.filter(email='test@gmail.com'):
		User.objects.create_superuser('test@gmail.com', '12345689!')
	driver.implicitly_wait(10)
	driver.get('%s%s' % (server_url, '/admin'))
	driver.find_element_by_id('id_username').send_keys('test@gmail.com')
	driver.find_element_by_id('id_password').send_keys('12345689!')
	driver.find_element_by_tag_name('button').click()


def create_product_listing_page() -> None:
	product_listing_page = ProductListingsPage(
		title='Products',
		title_en='Products',
	)
	home_page = HomePage.objects.all()[0]
	home_page.title = 'Home Page'
	home_page.title_en = 'Home Page'
	home_page.add_child(instance=product_listing_page)
	home_page.save()
	product_listing_page.save()


def create_wagtail_image() -> Image:
	image_path = BASE_DIR + '/shop/static/shop/img/test/test.webp'
	file_mock = SimpleUploadedFile(
		name='test_image.jpg', 
		content=open(image_path, 'rb').read(), 
		content_type='image/jpeg'
	)
	try:
		image = Image.objects.create(title='file_mock.jpg', file=file_mock)
	except Exception:
		image_path = BASE_DIR + '/shop/static/shop/img/test/test.webp'
		file_mock = SimpleUploadedFile(
			name='test_image.jpg', 
			content=open(image_path, 'rb').read(), 
			content_type='image/jpeg'
		)
		image = Image.objects.create(title='file_mock.jpg', file=file_mock)
	return image


def create_product_category() -> ProductCategory:
	wagtail_images = Image.objects.all()
	if wagtail_images:
		wagtail_image = wagtail_images[0]
	else:
		wagtail_image = create_wagtail_image()
	return ProductCategory.objects.create(
		name='Jackets',
		name_en='Jackets',
		slug='jackets',
		image=wagtail_image
	)


def create_size_category() -> SizeCategory:
	return SizeCategory.objects.create(
		name='Jackets',
		name_en='Jackets',
		slug='jackets'
	)


def create_product_sizes(size_category: SizeCategory) -> List[ProductSize]:
	product_sizes = []
	product_size = ProductSize.objects.create(
		name='Small',
		name_en='Small',
		slug='small',
		order_sequence=1
	)
	product_size.size_categories.add(size_category)
	product_sizes.append(product_size)
	product_size = ProductSize.objects.create(
		name='Medium',
		name_en='Medium',
		slug='medium',
		order_sequence=2
	)
	product_size.size_categories.add(size_category)
	product_sizes.append(product_size)
	product_size = ProductSize.objects.create(
		name='Large',
		name_en='Large',
		slug='large',
		order_sequence=3
	)
	product_size.size_categories.add(size_category)
	product_sizes.append(product_size)
	return product_sizes
