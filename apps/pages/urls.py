from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('legal/<slug:slug>/', views.legal, name='legal'),
    path('age-gate/', views.age_gate_set, name='age_gate'),
]
