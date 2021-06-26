from shop.models import Setting


def two_decimals(s: float) -> str:
	return '%.2f' % s


def display_currency_price(price: int) -> str:
	currency = Setting.get_CURRENCY()
	currency_code = Setting.get_CURRENCY_CODE()
	if currency_code == 'yen':
		return str(currency) + str(price)
	return currency + two_decimals(price / 100)


def convert_to_paypal_price(price: int) -> str:
	if Setting.get_CURRENCY() == 'yen':
		return str(price)
	return str(price / 100).replace(',', '.')
