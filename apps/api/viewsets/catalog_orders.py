from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.api.serializers.catalog import (
    BrandSerializer,
    CategorySerializer,
    ProductSerializer,
)
from apps.api.serializers.orders import OrderDetailSerializer, OrderSerializer
from apps.catalog.models import Brand, Category, Product
from apps.orders.models import Order


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


class MyOrdersViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_number'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer
