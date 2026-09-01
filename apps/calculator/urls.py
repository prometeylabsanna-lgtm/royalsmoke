from django.urls import path

from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.calculator_page, name='page'),
    path('results/', views.calculator_results, name='results'),
]
