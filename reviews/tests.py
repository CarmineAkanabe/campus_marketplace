from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from products.models import Product
from requestsystem.models import PurchaseRequest
from .models import Review

User = get_user_model()


class ReviewTest(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='pass', role=User.BUYER)
        self.seller = User.objects.create_user(username='seller', password='pass', role=User.SELLER)
        self.product = Product.objects.create(
            seller=self.seller,
            name='Tablet',
            description='A lightweight tablet',
            category='Electronics',
            price=249.99,
            condition=Product.CONDITION_NEW,
        )
        self.purchase_request = PurchaseRequest.objects.create(
            buyer=self.buyer,
            product=self.product,
            message='Interested in buying',
            status=PurchaseRequest.STATUS_ACCEPTED,
        )

    def test_review_create_after_request_accepted(self):
        self.client.login(username='buyer', password='pass')
        response = self.client.post(
            reverse('reviews:review_create', args=[self.purchase_request.pk]),
            {'rating': 5, 'comment': 'Excellent seller'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.seller, self.seller)
        self.assertEqual(review.rating, 5)
