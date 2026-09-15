from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.auth_views import (
    CartItemView,
    CartView,
    CheckoutView,
    LoginView,
    LogoutView,
    RegisterView,
)
from apps.api.viewsets.catalog_orders import (
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
    path('auth/register/', RegisterView.as_view(), name='api-register'),
    path('auth/login/', LoginView.as_view(), name='api-login'),
    path('auth/logout/', LogoutView.as_view(), name='api-logout'),
    path('cart/', CartView.as_view(), name='api-cart'),
    path('cart/items/<int:item_id>/', CartItemView.as_view(), name='api-cart-item'),
    path('checkout/', CheckoutView.as_view(), name='api-checkout'),
]
