from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from requestsystem.models import PurchaseRequest
from reviews.models import Review
from .models import Product

User = get_user_model()


class ProductViewsTest(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='seller', password='pass', role=User.SELLER)
        self.product = Product.objects.create(
            seller=self.seller,
            name='Smartphone',
            description='An affordable device',
            category='Electronics',
            price=199.99,
            condition=Product.CONDITION_NEW,
        )

    def test_product_list_contains_available_product(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_list_search_filters(self):
        response = self.client.get(reverse('products:product_list'), {'q': 'smart'})
        self.assertContains(response, self.product.name)

    def test_product_detail_view(self):
        response = self.client.get(reverse('products:product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.description)

    def test_product_detail_shows_review_link_for_accepted_buyer_request(self):
        buyer = User.objects.create_user(username='buyer', password='pass', role=User.BUYER)
        purchase_request = PurchaseRequest.objects.create(
            buyer=buyer,
            product=self.product,
            message='I want this product.',
            status=PurchaseRequest.STATUS_ACCEPTED,
        )

        self.client.force_login(buyer)
        response = self.client.get(reverse('products:product_detail', args=[self.product.pk]))

        self.assertContains(response, 'Leave seller review')
        self.assertContains(response, reverse('reviews:review_create', args=[purchase_request.pk]))

    def test_product_detail_hides_review_link_after_review(self):
        buyer = User.objects.create_user(username='buyer', password='pass', role=User.BUYER)
        PurchaseRequest.objects.create(
            buyer=buyer,
            product=self.product,
            message='I want this product.',
            status=PurchaseRequest.STATUS_COMPLETED,
        )
        Review.objects.create(buyer=buyer, seller=self.seller, rating=5, comment='Great seller.')

        self.client.force_login(buyer)
        response = self.client.get(reverse('products:product_detail', args=[self.product.pk]))

        self.assertNotContains(response, 'Leave seller review')
