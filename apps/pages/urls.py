from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('faq/', views.faq, name='faq'),
    path('legal/<slug:slug>/', views.legal, name='legal'),
    path('age-gate/', views.age_gate_set, name='age_gate'),
]
