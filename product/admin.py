from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from product import models, forms


class ProductMediasInline(admin.StackedInline):
    model = models.ProductMedia
    extra = 0
    fields = ['media']


class TecInfoNameAdmin(admin.StackedInline):
    model = models.TecInfoName
    extra = 0
    fields = ['name']


class CityInline(TranslationStackedInline):
    model = models.City
    extra = 0
    fields = ['name']


@admin.register(models.TechnicalInformation)
class TecInfoAdmin(admin.ModelAdmin):
    inlines = [TecInfoNameAdmin]


@admin.register(models.Product)
class ProductAdmin(TranslationAdmin):
    fieldsets = (
        ('Product Info', {"fields": ("main_image", 'info', 'colors', "category", "brand", 'price', 'discount_percentage', 'is_top', 'is_discount', 'is_popular')}),
        ("Product Name", {"fields": ("name_uz", "name_ru", "name_en")}),
    )
    inlines = [ProductMediasInline]


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


@admin.register(models.ProductTecInfo)
class ProductTecInfoAdmin(admin.ModelAdmin):
    form = forms.ProductTecInfoForm


@admin.register(models.ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User info', {"fields": ('first_name', 'last_name', 'phone_number', 'user')}),
        ("Location", {"fields": ("region", "city", "address", 'floor')}),
        ("Order info", {"fields": ("products", "product_count", "total_price", 'comment')}),
        ("Status", {"fields": ("status", "method_for_reception")}),
    )
    # readonly_fields = [
    #     'region', 'city', 'address', 'floor', 'products', 'product_count', 'total_price',
    #     'comment', 'first_name', 'last_name', 'phone_number', 'user',
    # ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(models.AnonymousUser)
class AnonymousUserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(models.Region)
class RegionAdmin(TranslationAdmin):
    inlines = [CityInline]