from django.utils.html import format_html
from wagtail.images.formats import Format, register_image_format


class CenteredImage(Format):
	def image_to_html(self, image, alt_text, extra_attributes=None):
		default_html = super().image_to_html(image, alt_text, extra_attributes)
		return format_html(
			'<div class="flex justify-center my-4">{}</div>', 
		default_html, alt_text)

register_image_format(
	CenteredImage('centered_image', 'Centered image', 'max-w-full', 'original')
)


class LeftImage(Format):
	def image_to_html(self, image, alt_text, extra_attributes=None):
		default_html = super().image_to_html(image, alt_text, extra_attributes)
		return format_html(
			'<div class="flex justify-start my-4">{}</div>', 
		default_html, alt_text)

register_image_format(
	LeftImage('left_image', 'Left aligned image', 'max-w-full', 'original')
)


class RightImage(Format):
	def image_to_html(self, image, alt_text, extra_attributes=None):
		default_html = super().image_to_html(image, alt_text, extra_attributes)
		return format_html(
			'<div class="flex justify-end my-4">{}</div>', 
		default_html, alt_text)

register_image_format(
	RightImage('right_image', 'Right aligned image', 'max-w-full', 'original')
)
