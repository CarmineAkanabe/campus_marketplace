from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('buyer/', views.buyer_dashboard, name='buyer_dashboard'),
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]
