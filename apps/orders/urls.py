from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('thank-you/<str:order_number>/', views.thank_you, name='thank_you'),
]
