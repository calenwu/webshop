import time
import shop.tests.utilities as utils

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from account.models import User
from shop.models import ProductPage, ProductColorImage, ProductColorQuantity


class SeleniumTestCase(StaticLiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.driver = utils.get_driver()

	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()
		super().tearDownClass()

	def setUp(self):
		super(SeleniumTestCase, self).setUp()

	@override_settings(DEBUG=True)
	def test_product_inlines_get_created(self):
		"""
		Test if Product, Product Colors and Product Color Image can be created at the same time,
		"""
		pass

	@override_settings(DEBUG=True)
	def test_product_inlines_get_created_after_being_empty_previously(self):
		"""
		Test if Product Color Image can be created when previously there have not been Product Color Images.
		"""
		pass
