from django.conf import settings


class Order(object):
	def __init__(self, request):
		"""
		Initialize the cart.
		"""
		self.session = request.session
		order = self.session.get(settings.ORDER_SESSION_ID)
		if not order:
			# save an empty order in the session
			order = self.session[settings.ORDER_SESSION_ID] = {}
		self.order = order

	def set_address(self, form_cleaned_data):
		"""
		Save address in cookies
		"""
		self.order = form_cleaned_data
		self.save()

	def save(self):
		"""
		Update the session order
		"""
		self.session[settings.ORDER_SESSION_ID] = self.order
		# mark the session as "modified" to make sure it is saved
		self.session.modified = True

	def clear(self):
		"""
		Clear order information
		"""
		self.session[settings.ORDER_SESSION_ID] = {}
		self.session.modified = True
