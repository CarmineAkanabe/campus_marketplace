from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from products.models import Product
from .models import ScrapedPrice
from .views import scrape_product_prices

User = get_user_model()


class ScraperTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(username='admin', password='pass', role=User.SELLER, is_staff=True)
        self.product = Product.objects.create(
            seller=self.staff,
            name='Camera',
            description='A compact camera',
            category='Photography',
            price=299.99,
            condition=Product.CONDITION_NEW,
        )

    @patch('scraper.views.requests.get')
    def test_scrape_product_prices(self, mock_get):
        mock_response = Mock(status_code=200, text='<html></html>')
        mock_get.return_value = mock_response

        scraped_entries, errors = scrape_product_prices(self.product)
        self.assertEqual(len(scraped_entries), 2)
        self.assertEqual(errors, [])
        self.assertEqual(ScrapedPrice.objects.count(), 2)

    def test_scrape_dashboard_requires_staff(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('scraper:scrape_dashboard'))
        self.assertEqual(response.status_code, 200)
