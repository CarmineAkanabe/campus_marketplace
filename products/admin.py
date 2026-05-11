from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'availability_status', 'created_at')
    list_filter = ('availability_status', 'category', 'condition')
    search_fields = ('name', 'description', 'category')
