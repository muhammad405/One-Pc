from datetime import datetime

from rest_framework import serializers

from product import models


class ProductCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en',
        ]


class PopularProductCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en', 'icon'
        ]


class ProductBrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductBrand
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en',
        ]


class DiscountedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscountProduct
        fields = ['id', 'image']


class PopularProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PopularProduct
        fields = [
            'id', 'title_uz', 'title_ru', 'title_en', 'name_uz', 'name_ru', 'name_en',
            'description_uz', 'description_ru', 'description_en', 'banner',
        ]


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductColor
        fields = ['id', 'rgba_name']


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductMedia
        fields = [
            'id', 'media'
        ]


class TecInfoNameSerializerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TecInfoName
        fields = ['id', 'name']


class TecInfoSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField(method_name='get_data')

    class Meta:
        model = models.TechnicalInformation
        fields = ['id', 'name', 'data']

    def get_data(self, obj):
        data = models.TecInfoName.objects.filter(tec_info__id=obj.id)
        return TecInfoNameSerializerSerializer(data, many=True).data


class ProductTecInfoSerializer(serializers.ModelSerializer):
    tec_info_id = serializers.IntegerField(source='tec_info.id')
    tec_info = serializers.CharField(source='tec_info.name')
    tec_info_name_id = serializers.IntegerField(source='tec_info_name.id')
    tec_info_name = serializers.CharField(source='tec_info_name.name')

    class Meta:
        model = models.ProductTecInfo
        fields = ['tec_info_id', 'tec_info', 'tec_info_name_id', 'tec_info_name']


class ProductListSerializer(serializers.ModelSerializer):
    discount_price = serializers.SerializerMethodField(method_name='get_discount_price')
    colors = serializers.SerializerMethodField(method_name='get_colors')

    class Meta:
        model = models.Product
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en', 'price', 'main_image', 'discount_percentage', 'is_discount',
            'discount_price', 'colors',
        ]

    def get_colors(self, obj):
        colors = obj.colors
        return ProductColorSerializer(colors, many=True).data

    def get_discount_price(self, obj):
        discount_price = 0
        if obj.discount_percentage == 0 or obj.is_discount == False:
            return discount_price
        else:
            discount_price = obj.price - ((obj.price / 100) * obj.discount_percentage)
            return discount_price


class ProductDetailSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id')
    category_name = serializers.CharField(source='category.name')
    brand_id = serializers.IntegerField(source='brand.id')
    brand_name = serializers.CharField(source='brand.name')
    discount_price = serializers.SerializerMethodField(method_name='get_discount_price')
    medias = serializers.SerializerMethodField(method_name='get_product_medias')
    colors = serializers.SerializerMethodField(method_name='get_product_colors')
    infos = serializers.SerializerMethodField(method_name='get_infos')

    class Meta:
        model = models.Product
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en', 'category_id', 'category_name', 'brand_id', 'brand_name',
            'price', 'discount_percentage', 'discount_price', 'medias', 'colors', 'infos',
        ]

    def get_discount_price(self, obj):
        discount_price = 0
        if obj.discount_percentage == 0 or obj.is_discount == False:
            return discount_price
        else:
            discount_price = obj.price - ((obj.price / 100) * obj.discount_percentage)
            return discount_price

    def get_product_medias(self, obj):
        medias = models.ProductMedia.objects.filter(product__id=obj.id)
        return ProductMediaSerializer(medias, many=True).data

    def get_product_colors(self, obj):
        return ProductColorSerializer(obj.colors, many=True).data

    def get_infos(self, obj):
        product_tec_info = obj.info.all()
        print(product_tec_info)
        return ProductTecInfoSerializer(product_tec_info, many=True).data


class OrderProductItemSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all())
    count = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        product = attrs.get("product_id")
        if not product:
            raise serializers.ValidationError({"product_id": "Mahsulot topilmadi."})
        return attrs


class OrderCreateSerializer(serializers.ModelSerializer):
    products = OrderProductItemSerializer(many=True)

    class Meta:
        model = models.OrderProduct
        fields = [
            'first_name', 'last_name', 'method_for_reception',
            'region', 'city', 'address', 'floor', 'phone_number', 'comment',
            'products', 'total_price',
        ]

    def create(self, validated_data):
        user = models.AnonymousUser.objects.filter(session=self.context['session_id']).first()
        region = models.Region.objects.filter(id=validated_data['region'].id).first()
        if region is None:
            raise serializers.ValidationError({"message": "region is not found"})
        city = models.City.objects.filter(id=validated_data['city'].id).first()
        if city is None:
            raise serializers.ValidationError({"message": "city is not found"})
        products_data = validated_data.pop('products')

        product_count = len(products_data)
        order = models.OrderProduct.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            method_for_reception=validated_data['method_for_reception'],
            region=region,
            city=city,
            address=validated_data['address'],
            floor=validated_data['floor'],
            phone_number=validated_data['phone_number'],
            comment=validated_data['comment'],
            total_price=validated_data['total_price'],
            user=user,
            status=models.NEW_ORDER,
            product_count=product_count,
        )
        for product_data in products_data:
            models.OrderProductItem.objects.create(
                order=order,
                product=product_data['product_id'],
                count=product_data['count']
            )

        return {
            "message": 'Order successfully created'
        }


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderProduct
        fields = [
            'id', 'status', 'created_at', 'product_count', 'total_price',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        created_at = representation['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        representation['created_at'] = created_at.strftime('%Y-%m-%d %H:%M:%S')
        return representation


class CompareProductSerializer(serializers.Serializer):
    product_ids = serializers.ListSerializer(
        child=serializers.IntegerField(), required=True, min_length=2, max_length=2
    )

    def validate_product_ids(self, value):
        if len(value) != 2:
            raise serializers.ValidationError("Iltimos, faqat ikki mahsulotni tanlang.")
        return value
