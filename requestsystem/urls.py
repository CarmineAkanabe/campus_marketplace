from django.urls import path

from . import views

app_name = 'requestsystem'

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('create/<int:product_id>/', views.request_create, name='request_create'),
    path('seller/', views.seller_request_list, name='seller_request_list'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
]
