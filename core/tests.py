from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from unittest.mock import Mock, patch
import requests

from core.services import convert_xaf_price
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

    def test_home_empty_state_renders_without_products(self):
        Product.objects.all().delete()
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No products available yet')

    def test_about_page_displays_team_members(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Abanda Ambrouise')
        self.assertContains(response, 'Serge')


class CurrencyServiceTests(TestCase):
    def setUp(self):
        cache.clear()

    @patch('core.services.requests.get')
    def test_convert_xaf_price_returns_values(self, mock_get):
        response = Mock()
        response.json.return_value = {'rate': 1.1}
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        converted = convert_xaf_price('10000.00')

        self.assertEqual(converted['USD'].as_tuple().exponent, -2)
        self.assertEqual(str(converted['USD']), '16.77')
        self.assertEqual(str(converted['EUR']), '15.24')

    @patch('core.services.requests.get')
    def test_convert_xaf_price_fails_gracefully(self, mock_get):
        mock_get.side_effect = requests.RequestException('network down')

        self.assertEqual(convert_xaf_price('10000.00'), {})


class ProjectCleanupTests(TestCase):
    def test_scraper_is_not_installed(self):
        self.assertNotIn('scraper', settings.INSTALLED_APPS)

    def test_seed_demo_data_is_rerunnable(self):
        call_command('seed_demo_data')
        call_command('seed_demo_data')

        User = get_user_model()
        self.assertEqual(User.objects.filter(username='demo_seller').count(), 1)
        self.assertEqual(User.objects.filter(username='demo_buyer').count(), 1)
        self.assertEqual(Product.objects.filter(seller__username='demo_seller').count(), 4)
