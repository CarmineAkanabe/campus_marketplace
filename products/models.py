from django.conf import settings
from django.db import models


class Product(models.Model):
    CONDITION_NEW = 'new'
    CONDITION_USED = 'used'
    CONDITION_CHOICES = [
        (CONDITION_NEW, 'New'),
        (CONDITION_USED, 'Used'),
    ]

    AVAILABILITY_AVAILABLE = 'available'
    AVAILABILITY_SOLD = 'sold'
    AVAILABILITY_CHOICES = [
        (AVAILABILITY_AVAILABLE, 'Available'),
        (AVAILABILITY_SOLD, 'Sold'),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default=CONDITION_USED)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    availability_status = models.CharField(max_length=15, choices=AVAILABILITY_CHOICES, default=AVAILABILITY_AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
