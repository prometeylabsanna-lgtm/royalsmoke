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
from apps.mobile.api import (
    MobileBrandViewSet,
    MobileLegalPageViewSet,
    MobileScreenViewSet,
    mobile_bundle_view,
    mobile_settings_view,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='api-categories')
router.register('brands', BrandViewSet, basename='api-brands')
router.register('products', ProductViewSet, basename='api-products')
router.register('my/orders', MyOrdersViewSet, basename='api-my-orders')
router.register('app/brands', MobileBrandViewSet, basename='api-app-brands')
router.register('app/screens', MobileScreenViewSet, basename='api-app-screens')
router.register('app/pages', MobileLegalPageViewSet, basename='api-app-pages')

urlpatterns = [
    path('', include(router.urls)),
    path('calculator/', calculator_api, name='api-calculator'),
    path('auth/register/', RegisterView.as_view(), name='api-register'),
    path('auth/login/', LoginView.as_view(), name='api-login'),
    path('auth/logout/', LogoutView.as_view(), name='api-logout'),
    path('cart/', CartView.as_view(), name='api-cart'),
    path('cart/items/<int:item_id>/', CartItemView.as_view(), name='api-cart-item'),
    path('checkout/', CheckoutView.as_view(), name='api-checkout'),
    path('app/settings/', mobile_settings_view, name='api-app-settings'),
    path('app/bundle/', mobile_bundle_view, name='api-app-bundle'),
]
