from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from apps.catalog.models import Brand, Category, Product, ProductVariant
from apps.orders.models import Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'kind', 'parent', 'image', 'description')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug', 'country', 'logo', 'short_description')


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = (
            'id', 'name', 'slug', 'length_mm', 'ring_gauge', 'shape',
            'price', 'old_price', 'sku', 'stock', 'image',
        )


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    variants = VariantSerializer(many=True, read_only=True)
    display_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'sku', 'brand', 'category', 'short_story',
            'description', 'tasting_notes', 'wrapper', 'binder', 'filler',
            'country', 'strength', 'smoke_time', 'base_price', 'old_price',
            'currency', 'display_price', 'variants', 'video_url',
        )


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filterset_fields = ('kind', 'parent')
    search_fields = ('name',)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    search_fields = ('name', 'country')


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.on_storefront().with_relations()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filterset_fields = ('strength', 'country', 'brand__slug', 'category__slug', 'tags__slug')
    search_fields = ('name', 'brand__name', 'description', 'short_story')
    ordering_fields = ('base_price', 'created_at', 'name', 'sort_order')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'order_number', 'status', 'total', 'currency', 'created_at',
            'delivery_service', 'payment_method',
        )


class MyOrdersViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(user=user)
