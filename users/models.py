from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    BUYER = 'buyer'
    SELLER = 'seller'
    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username

    def is_buyer(self):
        return self.role == self.BUYER

    def is_seller(self):
        return self.role == self.SELLER

    def average_rating(self):
        from django.db.models import Avg

        return self.reviews_received.aggregate(avg=Avg('rating'))['avg'] or 0

    @property
    def unread_notifications_count(self):
        return self.notifications.filter(is_read=False).count()
