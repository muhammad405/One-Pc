from django_filters import rest_framework as filters

from product import models


class ProductFilter(filters.FilterSet):
    brand = filters.BaseInFilter(field_name='brand__id', lookup_expr='in')
    color = filters.BaseInFilter(field_name='colors__id', lookup_expr='in')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte', label="Min Price")
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte', label="Max Price")
    info = filters.BaseInFilter(field_name='info__tec_info_name__id', lookup_expr='in')

    class Meta:
        model = models.Product
        fields = ['is_discount', 'brand', 'min_price', 'max_price', 'info']