from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from apps.catalog.models import Product
from apps.core.i18n_views import set_language
from apps.core.views import health, healthz
from apps.orders import views as order_views
from apps.pages.sitemaps import BlogPostSitemap, StaticPagesSitemap
from django.contrib.sitemaps import GenericSitemap

info_dict = {
    'queryset': Product.objects.filter(is_active=True),
    'date_field': 'updated_at',
}

sitemaps = {
    'static': StaticPagesSitemap,
    'products': GenericSitemap(info_dict, priority=0.7),
    'blog': BlogPostSitemap,
}

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('apps.pwa.urls')),
    path('i18n/setlang/', set_language, name='set_language'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/v1/', include('apps.api.urls')),
    path('health/', health, name='health'),
    path('healthz/', healthz, name='healthz'),
    path('orders/liqpay/callback/', order_views.liqpay_callback, name='orders_liqpay_callback'),
    path('orders/liqpay/result/', order_views.liqpay_result, name='orders_liqpay_result'),
    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
    ),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),
]

urlpatterns += i18n_patterns(
    path('', include('apps.pages.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('cart/', include('apps.cart.urls')),
    path('', include('apps.accounts.urls')),
    path('orders/', include('apps.orders.urls')),
    path('booking/', include('apps.booking.urls')),
    path('calculator/', include('apps.calculator.urls')),
    path('service/', include('apps.leads.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
