from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class DashboardTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='pass', role=User.BUYER)
        self.seller = User.objects.create_user(username='seller', password='pass', role=User.SELLER)

    def test_buyer_dashboard_access(self):
        self.client.login(username='buyer', password='pass')
        response = self.client.get(reverse('dashboard:buyer_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_seller_dashboard_access(self):
        self.client.login(username='seller', password='pass')
        response = self.client.get(reverse('dashboard:seller_dashboard'))
        self.assertEqual(response.status_code, 200)
