from django.urls import path

from apps.pwa import views

app_name = 'pwa'

urlpatterns = [
    path('manifest.webmanifest', views.manifest, name='manifest'),
    path('sw.js', views.service_worker, name='sw'),
    path('pwa/offline/', views.offline_shell, name='offline'),
    path('pwa/offline-catalog.json', views.offline_catalog_json, name='offline_catalog'),
    path('pwa/vapid-public-key/', views.vapid_key, name='vapid_key'),
    path('pwa/push/subscribe/', views.push_subscribe, name='push_subscribe'),
    path('pwa/push/bind/', views.push_bind_email, name='push_bind'),
]
