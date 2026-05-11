from django.urls import path

from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    path('seller/', views.seller_analytics, name='seller_analytics'),
]
