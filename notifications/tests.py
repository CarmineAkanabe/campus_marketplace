from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Notification

User = get_user_model()


class NotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass', role=User.BUYER)
        Notification.objects.create(user=self.user, title='Hello', message='Test message')

    def test_notification_list_view(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('notifications:notification_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')

    def test_mark_notification_as_read(self):
        self.client.login(username='user', password='pass')
        notification = Notification.objects.first()
        response = self.client.get(reverse('notifications:mark_as_read', args=[notification.pk]))
        self.assertEqual(response.status_code, 302)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
