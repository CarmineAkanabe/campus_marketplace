from django.conf import settings
from django.db import models

from products.models import Product


class SearchQuery(models.Model):
    """Track search queries for analytics."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='search_queries')
    query = models.CharField(max_length=255)
    category_filter = models.CharField(max_length=100, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']
        indexes = [
            models.Index(fields=['-searched_at']),
            models.Index(fields=['query']),
        ]

    def __str__(self):
        return f"'{self.query}' at {self.searched_at}"


class ProductAnalytics(models.Model):
    """Aggregated analytics for products."""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='analytics')
    view_count = models.PositiveIntegerField(default=0)
    request_count = models.PositiveIntegerField(default=0)
    completed_count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Product Analytics"

    def __str__(self):
        return f"Analytics for {self.product}"
