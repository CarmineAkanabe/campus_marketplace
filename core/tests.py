from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from products.models import Product

User = get_user_model()


class CoreTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='seller', password='pass', role=User.SELLER)
        self.available_product = Product.objects.create(
            seller=self.seller,
            name='Notebook',
            description='College notebook',
            category='School Supplies',
            price=2.99,
            condition=Product.CONDITION_NEW,
        )
        self.sold_product = Product.objects.create(
            seller=self.seller,
            name='Old Textbook',
            description='Used textbook',
            category='Books',
            price=10.00,
            condition=Product.CONDITION_USED,
            availability_status=Product.AVAILABILITY_SOLD,
        )

    def test_home_displays_available_products(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.available_product.name)
        self.assertNotContains(response, self.sold_product.name)
