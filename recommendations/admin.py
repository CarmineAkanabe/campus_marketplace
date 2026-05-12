from django.contrib import admin

from .models import ProductView


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'viewed_at')
    list_filter = ('viewed_at', 'product__category')
    search_fields = ('user__username', 'product__name', 'product__category')
