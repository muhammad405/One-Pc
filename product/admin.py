from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from product import models, forms
import os
import sys
import subprocess
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages

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

class OrderItemInline(admin.StackedInline):
    model = models.OrderProductItem
    extra = 0
    fields = ['product', 'count']
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj):
        return False

@admin.register(models.TechnicalInformation)
class TecInfoAdmin(admin.ModelAdmin):
    inlines = [TecInfoNameAdmin]


@admin.register(models.Product)
class ProductAdmin(TranslationAdmin):
    fieldsets = (
        ('Product Info', {"fields": ("main_image", 'info', 'colors', "category", "brand", 'price', 'discount_percentage', 'is_top', 'is_discount', 'is_popular', 'item', 'quantity_left',)}),
        ("Product Name", {"fields": ("name_uz", "name_ru", "name_en")}),
    )
    inlines = [ProductMediasInline]
    list_display = ['item', 'name_uz', 'name_ru', 'name_en', 'category', 'main_image']
    list_editable = ['name_uz', 'name_ru', 'name_en', 'category', 'main_image']
    search_fields = ('item', 'name_uz', 'name_ru', 'name_en')
    list_filter = ['category']
    change_list_template = "admin/custom_changelist.html"

    def changelist_view(self, request, extra_context=None):
        products = models.Product.objects.all()
        product_count = products.count()
        product_with_image = products.filter(main_image__isnull=False).exclude(main_image='').count()
        product_without_image = product_count - product_with_image
        extra_context = extra_context or {}
        extra_context['product_count'] = product_count
        extra_context['product_with_image'] = product_with_image
        extra_context['product_without_image'] = product_without_image
        return super().changelist_view(request, extra_context=extra_context)

    # 🔹 Custom URL qo‘shamiz
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("run-utils/", self.admin_site.admin_view(self.run_utils), name="run-utils"),
        ]
        return custom_urls + urls

    # 🔹 utilts.py ni ishlatadigan view
    def run_utils(self, request):
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            utilts_path = os.path.join(project_root, "utils.py")

            # subprocess orqali ishlatamiz
            subprocess.run([sys.executable, utilts_path], check=True)

            self.message_user(request, "✅ utils.py muvaffaqiyatli ishga tushdi", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"❌ Xatolik: {e}", messages.ERROR)

        return redirect("..")




@admin.register(models.ProductCategory)
class ProductCategoryAdmin(TranslationAdmin):
    list_display = ['name', 'is_popular', 'products_count']
    list_display_links = list_display
    list_filter = ['is_popular']
    def products_count(self, obj):
        return obj.products.count()

@admin.register(models.DiscountProduct)
class DiscountProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_uz', 'product']

@admin.register(models.PopularProduct)
class PopularProductAdmin(TranslationAdmin):
    fieldsets = (
        ('Banner', {"fields": ('banner', 'product')}),
        ("Uzbek tilida", {"fields": ("title_uz", "name_uz", "description_uz")}),
        ("Rus tilida", {"fields": ("title_ru", "name_ru", "description_ru")}),
        ("Ingliz tilida", {"fields": ("title_en", "name_en", "description_en")}),
    )
    list_display = ['name', 'title']
    list_display_links = list_display

@admin.register(models.ProductTecInfo)
class ProductTecInfoAdmin(admin.ModelAdmin):
    form = forms.ProductTecInfoForm

@admin.register(models.ProductBrand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = list_display
