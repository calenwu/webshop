import logging
import random
import string
from django import template

from streams.blocks import BannerCarouselBlock

register = template.Library()
logger = logging.getLogger('django')


@register.simple_tag
def random_string():
	allowed_chars = ''.join(string.ascii_letters)
	return ''.join(random.choice(allowed_chars) for _ in range(8))


@register.simple_tag
def full_width(block) -> bool:
	if isinstance(block.block, BannerCarouselBlock):
		return True
	return False


@register.simple_tag
def get_banner_carousel_block_url(slide) -> bool:
	if slide['page']:
		temp = slide['page'].url
		return temp[3:len(temp)]
	else:
		return slide['url']
