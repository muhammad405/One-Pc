from django.urls import path

from product import views


urlpatterns = [
    path('search/', views.SearchApiView.as_view(), name='search'),
    # product brand
    path('product-brand/list/', views.ProductBrandListApiView.as_view(), name='product-brand-list'),
    # product color
    path('product-color/list/', views.ProductColorListSerializer.as_view(), name='product-color-list'),
    # product category
    path('category/list/', views.ProductCategoryListApiView.as_view(), name='product-category-list'),
    path('category/<int:category_id>/', views.ProductLByCategoryListApiView.as_view(),name='product-by-category-list'),
    path('category/info/<int:category_id>/', views.CategoryInfoApiView.as_view(), name='category-infos'),
    path('category/get_max_min_price/<category_id>/', views.GetMinAndMaxPriceApiView.as_view(), name='get_max_and_min_price'),
    # discounted product
    path('discounted-product/list/', views.DiscountedProductListApiView.as_view(), name='discounted-product'),
    path('most-popular-product/list/', views.PopularProductListApiView.as_view(), name='most-popular-product-list'),
    # product apis for home page
    path('product/new/list/', views.NewProductListApiView.as_view(), name='new-product-list'),
    path('product/top/list/', views.TopProductListApiView.as_view(), name='top-product-list'),
    path('product/popular/list/', views.PopularProductApiView.as_view(), name='popular-product-list'),
    path('product/<int:product_id>/', views.ProductDetailApiView.as_view(), name='product-detail'),
    path('product/similar-products/<int:product_id>/', views.SimilarProductListApiView.as_view(), name='product-detail'),
    path('product/<int:brand_id>/list/', views.ProductListByBrandIdApiView.as_view()),
    # product order
    path('order/create/', views.OrderCreateApiView.as_view(), name='order-create'),
    path('get-methods/', views.GetOrderMethodForReceptionApiView.as_view(), name='get-methods'),
    # compare products
    path('compare/', views.CompareProductApiView.as_view(), name='compare-products'),
]