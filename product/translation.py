from modeltranslation.translator import TranslationOptions, register

from product import models


@register(models.ProductCategory)
class ProductCategoryTranslation(TranslationOptions):
    fields = ['name']


@register(models.ProductBrand)
class ProductBrandTranslation(TranslationOptions):
    fields = ['name']


@register(models.Product)
class ProductTranslation(TranslationOptions):
    fields = ['name',]


@register(models.ProductInfo)
class ProductInfoTranslation(TranslationOptions):
    fields = ['name']


@register(models.ProductTecInfo)
class ProductTecInfoTranslation(TranslationOptions):
    fields = ['info_name', 'info_text',]


@register(models.PopularProduct)
class PopularProductTranslation(TranslationOptions):
    fields = ['title', 'name', 'description']
