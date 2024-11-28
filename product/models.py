from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class ProductCategory(BaseModel):
    name = models.CharField(max_length=250)
    is_top = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')


class ProductBrand(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product brand')
        verbose_name_plural = _('product brands')


class Product(BaseModel):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='product_categories')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name='product_brands')
    price = models.PositiveBigIntegerField(default=0)
    discount_percentage = models.PositiveIntegerField(default=0)
    is_discount = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class ProductColor(BaseModel):
    rgba_name = models.CharField(max_length=250)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_colors')

    def __str__(self):
        return self.rgba_name

    class Meta:
        verbose_name = _('product color')
        verbose_name_plural = _('product colors')


class ProductMedia(BaseModel):
    video = models.FileField(null=True, blank=True, upload_to='product/product-media')
    image = models.ImageField(null=True, blank=True, upload_to='product/product-media')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_medias')

    def __str__(self):
        return self.image.name or self.video.name

    class Meta:
        verbose_name = _('product media')
        verbose_name_plural = _('product medias')


class ProductTecInfo(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tec_infos')
    info_name = models.CharField(max_length=250)
    info_text = models.CharField(max_length=250)

    def __str__(self):
        return self.info_name

    class Meta:
        verbose_name = _('product tech info')
        verbose_name_plural = _('product tech infos')


class ProductInfo(BaseModel):
    name = models.CharField(max_length=250)
    product_tec_info = models.ForeignKey(ProductTecInfo, on_delete=models.CASCADE, related_name='product_infos')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product info')
        verbose_name_plural = _('product infos')


class DiscountProduct(BaseModel):
    image = models.ImageField(upload_to='product/discount-product')

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = _('discount product')
        verbose_name_plural = _('discount products')


class PopularProduct(BaseModel):
    title = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    banner = models.ImageField(upload_to='product/popular-product')
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('popular product')
        verbose_name_plural = _('popular products')
