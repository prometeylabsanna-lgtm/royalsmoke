from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('account/login/', views.login_view, name='login'),
    path('account/register/', views.register_view, name='register'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/cabinet/', views.cabinet, name='cabinet'),
    path('wishlist/', views.wishlist_detail, name='wishlist'),
    path('wishlist/toggle/', views.wishlist_toggle, name='wishlist_toggle'),
]
