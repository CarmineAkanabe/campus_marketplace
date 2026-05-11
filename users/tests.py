from django.contrib.auth import get_user_model
from django.test import TestCase

from reviews.models import Review

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='pass', role=User.BUYER)
        self.seller = User.objects.create_user(username='seller', password='pass', role=User.SELLER)

    def test_role_helpers(self):
        self.assertTrue(self.buyer.is_buyer())
        self.assertFalse(self.buyer.is_seller())
        self.assertTrue(self.seller.is_seller())
        self.assertFalse(self.seller.is_buyer())

    def test_average_rating_empty(self):
        self.assertEqual(self.seller.average_rating(), 0)

    def test_average_rating(self):
        Review.objects.create(buyer=self.buyer, seller=self.seller, rating=4, comment='Good')
        Review.objects.create(buyer=self.buyer, seller=self.seller, rating=5, comment='Great')
        self.assertEqual(self.seller.average_rating(), 4.5)
