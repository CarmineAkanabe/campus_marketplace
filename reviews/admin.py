from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'seller', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('buyer__username', 'seller__username', 'comment')
