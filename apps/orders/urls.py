from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('thank-you/<str:order_number>/', views.thank_you, name='thank_you'),
    path('pay/<str:order_number>/', views.pay, name='pay'),
    path('np/cities/', views.np_cities, name='np_cities'),
    path('np/warehouses/', views.np_warehouses, name='np_warehouses'),
    path('np/cost/', views.np_cost, name='np_cost'),
]
