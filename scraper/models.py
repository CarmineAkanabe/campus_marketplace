from django.conf import settings
from django.db import models

from products.models import Product


class ScrapedPrice(models.Model):
    """Store price data scraped from external sources."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='scraped_prices')
    source_name = models.CharField(max_length=100)
    source_url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    scraped_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scraped_at']
        indexes = [
            models.Index(fields=['product', '-scraped_at']),
        ]

    def __str__(self):
        return f"{self.source_name} - {self.product.name}: FCFA {self.price}"

    def price_difference(self):
        """Calculate difference between this scraped price and our price."""
        if self.product.price:
            return float(self.price) - float(self.product.price)
        return 0

    def price_difference_percent(self):
        """Calculate percentage difference."""
        if self.product.price and float(self.product.price) > 0:
            return (self.price_difference() / float(self.product.price)) * 100
        return 0


class PriceScrapeLog(models.Model):
    """Log of scraping operations."""
    SOURCES = [
        ('amazon', 'Amazon'),
        ('ebay', 'eBay'),
        ('other', 'Other'),
    ]
    
    source = models.CharField(max_length=50, choices=SOURCES)
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Success'),
            ('partial', 'Partial'),
            ('failed', 'Failed'),
        ]
    )
    products_scraped = models.PositiveIntegerField(default=0)
    prices_found = models.PositiveIntegerField(default=0)
    errors = models.TextField(blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scraped_at']

    def __str__(self):
        return f"{self.source} - {self.status} at {self.scraped_at}"
