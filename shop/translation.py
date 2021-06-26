from modeltranslation.decorators import register
from modeltranslation.translator import translator, TranslationOptions
from .models import (
	ProductListingsPage,
	ProductCategory,
	SizeCategory,
	ProductColor,
	ProductSize,
	ProductPage,
	ProductImages,
	ProductColorImage
)


@register(ProductListingsPage)
class ProductListingsPageOptions(TranslationOptions):
	"""
	Product listing translation fields
	"""
	fields = ['content', ]


@register(ProductCategory)
class ProductCategoryOptions(TranslationOptions):
	"""
	Product category variable translation fields
	"""
	fields = ['name', ]


@register(SizeCategory)
class SizeCategoryOptions(TranslationOptions):
	"""
	Size category variable translation fields
	"""
	fields = ['name', ]


@register(ProductSize)
class ProductSizeOptions(TranslationOptions):
	"""
	Product size variable translation fields
	"""
	fields = ['name', ]


@register(ProductPage)
class ProductPageOptions(TranslationOptions):
	"""
	Product page variable translation fields
	"""
	fields = ['details', 'content', 'reference_buttons']


@register(ProductImages)
class ProductImagesOptions(TranslationOptions):
	"""
	Product image variable translation fields
	"""
	fields = ['description', ]


@register(ProductColorImage)
class ProductColorImageOptions(TranslationOptions):
	"""
	ProductColor image variable translation fields
	"""
	fields = ['description', ]


@register(ProductColor)
class ProductColorTr(TranslationOptions):
	"""
	ProductColor variable translation fields
	"""
	fields = ['color', ]

