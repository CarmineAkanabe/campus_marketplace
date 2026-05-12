from django.contrib import admin

from .models import ProductAnalytics, SearchQuery


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'category_filter', 'user', 'searched_at')
    list_filter = ('category_filter', 'searched_at')
    search_fields = ('query', 'category_filter', 'user__username')


@admin.register(ProductAnalytics)
class ProductAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('product', 'view_count', 'request_count', 'completed_count', 'last_updated')
    search_fields = ('product__name',)
