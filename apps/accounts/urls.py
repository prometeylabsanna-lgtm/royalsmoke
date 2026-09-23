from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('account/login/', views.login_view, name='login'),
    path('account/register/', views.register_view, name='register'),
    path('account/logout/', views.logout_view, name='logout'),
    path('account/cabinet/', views.cabinet, name='cabinet'),
    path('account/password/', views.password_change_view, name='password_change'),
    path('account/delete/', views.delete_account_view, name='delete_account'),
    path('wishlist/', views.wishlist_detail, name='wishlist'),
    path('wishlist/toggle/', views.wishlist_toggle, name='wishlist_toggle'),
]
