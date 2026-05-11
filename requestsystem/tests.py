from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from products.models import Product
from .models import PurchaseRequest

User = get_user_model()


class PurchaseRequestTest(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='pass', role=User.BUYER)
        self.seller = User.objects.create_user(username='seller', password='pass', role=User.SELLER)
        self.product = Product.objects.create(
            seller=self.seller,
            name='Laptop',
            description='A reliable laptop',
            category='Electronics',
            price=499.99,
            condition=Product.CONDITION_USED,
        )

    def test_buyer_can_create_purchase_request(self):
        self.client.login(username='buyer', password='pass')
        response = self.client.post(
            reverse('requestsystem:request_create', args=[self.product.pk]),
            {'message': 'I am interested'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PurchaseRequest.objects.count(), 1)
        request_item = PurchaseRequest.objects.first()
        self.assertEqual(request_item.status, PurchaseRequest.STATUS_PENDING)
        self.assertEqual(request_item.buyer, self.buyer)

    def test_seller_can_update_request_status(self):
        request_item = PurchaseRequest.objects.create(
            buyer=self.buyer,
            product=self.product,
            message='Please send details',
        )
        self.client.login(username='seller', password='pass')
        response = self.client.post(
            reverse('requestsystem:request_detail', args=[request_item.pk]),
            {'status': PurchaseRequest.STATUS_ACCEPTED},
        )
        self.assertEqual(response.status_code, 302)
        request_item.refresh_from_db()
        self.assertEqual(request_item.status, PurchaseRequest.STATUS_ACCEPTED)
