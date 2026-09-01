from django.urls import path

from . import views

app_name = 'leads'

urlpatterns = [
    path('b2b/', views.b2b_page, name='b2b'),
    path('delivery/', views.delivery_page, name='delivery'),
    path('contact/', views.contact_page, name='contact'),
    path('callback/', views.callback, name='callback'),
]
