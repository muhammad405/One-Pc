from django.db.models import Q, Min, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, views, status, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from product import models, serializers, filters, paganation


class ProductCategoryListApiView(views.APIView):
    def get(self, request):
        queryset = models.ProductCategory.objects.all()
        serializer = serializers.ProductCategoryListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductBrandListApiView(views.APIView):
    def get(self, request):
        brands = models.ProductBrand.objects.all()
        serializer = serializers.ProductBrandListSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductColorListSerializer(views.APIView):
    def get(self, request):
        colors = models.ProductColor.objects.all()
        serializer = serializers.ProductColorSerializer(colors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DiscountedProductListApiView(views.APIView):
    def get(self, request):
        queryset = models.DiscountProduct.objects.all()
        serializer = serializers.DiscountedProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewProductListApiView(views.APIView):
    def get(self, request):
        queryset = models.Product.objects.order_by('-created_at')[:5]
        serializer = serializers.ProductListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularProductListApiView(views.APIView):
    def get(self, request):
        queryset = models.PopularProduct.objects.all()
        serializer = serializers.PopularProductListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopProductListApiView(views.APIView):
    def get(self, request):
        queryset = models.Product.objects.filter(is_top=True)[:5]
        serializer = serializers.ProductListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularProductApiView(views.APIView):
    def get(self, request):
        queryset = models.Product.objects.filter(is_popular=True)
        serializer = serializers.ProductListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductLByCategoryListApiView(generics.ListAPIView):
    serializer_class = serializers.ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProductFilter
    pagination_class = paganation.CustomPagination

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return models.Product.objects.filter(category__id=category_id)


class ProductDetailApiView(views.APIView):
    def get(self, request, product_id):
        try:
            product = models.Product.objects.get(id=product_id)
        except models.Product.DoesnotExist:
            return Response({'message': 'Product not found'})
        serializer = serializers.ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryInfoApiView(views.APIView):
    def get(self, request, category_id):
        data = models.TechnicalInformation.objects.filter(category__id=category_id)
        serializer = serializers.TecInfoSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SimilarProductListApiView(views.APIView):
    def get(self, request, product_id):
        product = models.Product.objects.filter(id=product_id).first()
        if product is None:
            return Response({"message": 'Product is not found'}, status=status.HTTP_400_BAD_REQUEST)
        products = models.Product.objects.filter(brand__id=product.brand.id, category__id=product.category.id).exclude(id=product_id)[:7]
        serializer = serializers.ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderCreateSerializer
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = serializers.OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetOrderMethodForReceptionApiView(views.APIView):
    def get(self, request):
        data = {
            'methods': models.OrderProduct.get_method_for_reception_list()
        }
        return Response(data)


class CompareProductApiView(generics.GenericAPIView):
    serializer_class = serializers.CompareProductSerializer
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product_ids = serializer.validated_data['product_ids']
        products = models.Product.objects.filter(id__in=product_ids)
        categories = products.values_list('category', flat=True).distinct()
        if categories.count() == 1:
            serializer = serializers.CompareProductListSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Products category is not  same'})


class SearchApiView(generics.GenericAPIView):
    serializer_class = serializers.SearchSerializer

    def post(self, request):
        serializer = serializers.SearchSerializer(data=request.data)
        serializer.is_valid()
        query =serializer.validated_data.get('search', '')
        products = models.Product.objects.filter(Q(name_uz__icontains=query) | Q(name_ru__icontains=query) | Q(name_en__icontains=query))
        categories = models.ProductCategory.objects.filter(Q(name_uz__icontains=query) | Q(name_ru__icontains=query) | Q(name_en__icontains=query))
        return Response({
            'products': serializers.ProductSearchSerializer(products, many=True).data,
            'categories': serializers.CategorySearchSerializer(categories, many=True).data,
        })


class GetMinAndMaxPriceApiView(views.APIView):
    def get(self, request, category_id):
        max_price = models.Product.objects.filter(category__id=category_id).aggregate(
            max_price=Max('price')
        )['max_price']
        min_price = models.Product.objects.filter(category__id=category_id).aggregate(
            min_price=Min('price')
        )['min_price']
        data = {
            'min_price': min_price,
            'max_price': max_price
        }
        return Response(data)

