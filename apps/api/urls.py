from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.serializers import (
    BrandViewSet,
    CategoryViewSet,
    MyOrdersViewSet,
    ProductViewSet,
)
from apps.calculator.views import calculator_api

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='api-categories')
router.register('brands', BrandViewSet, basename='api-brands')
router.register('products', ProductViewSet, basename='api-products')
router.register('my/orders', MyOrdersViewSet, basename='api-my-orders')

urlpatterns = [
    path('', include(router.urls)),
    path('calculator/', calculator_api, name='api-calculator'),
]
