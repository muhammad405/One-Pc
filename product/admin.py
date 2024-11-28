from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from product import models


class ProductInfoInline(TranslationStackedInline):
    model = models.ProductInfo
    fields = ['name']
    extra = 0


class ProductTecInfoInline(TranslationStackedInline):
    model = models.ProductTecInfo
    fields = ['link', 'info_name', 'info_text']
    readonly_fields = ['link']
    extra = 0

    def link(self, instance):
        url = f"/admin/course/club/{instance.id}/change/"
        return mark_safe(f'<a href="{url}">Kirish</a>')


class ProductMediasInline(admin.StackedInline):
    model = models.ProductMedia
    extra = 0
    fields = ['image', 'video']


class ProductColorInline(admin.StackedInline):
    model = models.ProductColor
    extra = 0
    fields = ['rgba_name',]


@admin.register(models.ProductTecInfo)
class ProductTecInfoAdmin(TranslationAdmin):
    inlines = [ProductInfoInline]

    def has_module_permission(self, request):
        return False


@admin.register(models.Product)
class ProductAdmin(TranslationAdmin):
    fieldsets = (
        ('Product Info', {"fields": ("category", "brand", 'price', 'discount_percentage', 'is_top', 'is_discount', 'is_popular')}),
        ("Product Name", {"fields": ("name_uz", "name_ru", "name_en")}),
    )
    inlines = [ProductTecInfoInline, ProductMediasInline, ProductColorInline]


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(TranslationAdmin):
    list_display = ['name', 'is_top', 'is_popular']
    list_display_links = list_display
    list_filter = ['is_top', 'is_popular']


@admin.register(models.ProductBrand)
class ProductBrandAdmin(TranslationAdmin):
    list_display = ['name']


@admin.register(models.DiscountProduct)
class DiscountProductAdmin(admin.ModelAdmin):
    list_display = ['image']


@admin.register(models.PopularProduct)
class PopularProductAdmin(TranslationAdmin):
    fieldsets = (
        ('Banner', {"fields": ('banner',)}),
        ("Uzbek tilida", {"fields": ("title_uz", "name_uz", "description_uz")}),
        ("Rus tilida", {"fields": ("title_ru", "name_ru", "description_ru")}),
        ("Ingliz tilida", {"fields": ("title_en", "name_en", "description_en")}),
    )
    list_display = ['name', 'title']
    list_display_links = list_display
