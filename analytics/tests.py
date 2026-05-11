from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import SearchQuery
from .views import get_popular_searches, track_search

User = get_user_model()


class AnalyticsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass', role=User.BUYER)

    def test_track_search_creates_search_query(self):
        track_search(self.user, 'laptop', 'Electronics')
        self.assertEqual(SearchQuery.objects.count(), 1)

    def test_get_popular_searches(self):
        track_search(self.user, 'laptop', 'Electronics')
        track_search(self.user, 'laptop', '')
        popular = get_popular_searches(limit=1)
        self.assertEqual(len(popular), 1)
        self.assertEqual(popular[0]['query'], 'laptop')
