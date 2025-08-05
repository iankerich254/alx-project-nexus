from django.test import TestCase
from django.utils import timezone
from polls.models import Poll, User
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta

class PollCreationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_poll_with_valid_expiry(self):
        future_date = timezone.now() + timedelta(days=2)
        data = {
            "title": "Valid Poll",
            "expiry": future_date.isoformat()
        }
        response = self.client.post('/api/polls/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poll.objects.count(), 1)

    def test_create_poll_with_past_expiry(self):
        past_date = timezone.now() - timedelta(days=1)
        data = {
            "title": "Invalid Poll",
            "expiry": past_date.isoformat()
        }
        response = self.client.post('/api/polls/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
