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


@register(models.PopularProduct)
class PopularProductTranslation(TranslationOptions):
    fields = ['title', 'name', 'description']


@register(models.Region)
class RegionTranslation(TranslationOptions):
    fields = ['name']


@register(models.City)
class CityTranslation(TranslationOptions):
    fields = ['name']