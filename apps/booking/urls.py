from django.urls import path

from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking_page, name='page'),
    path('slots/', views.booking_slots_partial, name='slots'),
    path('request/', views.booking_request, name='request'),
]
