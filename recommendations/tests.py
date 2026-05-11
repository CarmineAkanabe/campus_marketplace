from django.contrib.auth import get_user_model
from django.test import TestCase

from products.models import Product
from .models import ProductView
from .views import get_recommendations_for_user, track_product_view

User = get_user_model()


class RecommendationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass', role=User.BUYER)
        self.seller = User.objects.create_user(username='seller', password='pass', role=User.SELLER)
        self.viewed_product = Product.objects.create(
            seller=self.seller,
            name='Headphones',
            description='Noise cancelling',
            category='Audio',
            price=99.99,
            condition=Product.CONDITION_NEW,
        )
        self.recommendation_product = Product.objects.create(
            seller=self.seller,
            name='Speaker',
            description='Portable speaker',
            category='Audio',
            price=59.99,
            condition=Product.CONDITION_NEW,
        )

    def test_track_product_view_creates_record(self):
        track_product_view(self.user, self.viewed_product)
        self.assertEqual(ProductView.objects.filter(user=self.user, product=self.viewed_product).count(), 1)

    def test_recommendations_for_user(self):
        track_product_view(self.user, self.viewed_product)
        recommendations = get_recommendations_for_user(self.user, limit=2)
        self.assertIn(self.recommendation_product, recommendations)
