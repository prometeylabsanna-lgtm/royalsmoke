from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog_list, name='list'),
    path('search/', views.search_suggest, name='search'),
    path('compare/', views.compare_detail, name='compare'),
    path('compare/toggle/', views.compare_toggle, name='compare_toggle'),
    path('brand/<slug:slug>/', views.brand_detail, name='brand'),
    path('product/<slug:slug>/', views.product_detail, name='product'),
    path('<slug:slug>/', views.catalog_list, name='category'),
]
