from django.test import TestCase
from django.urls import reverse
from polls.models import Poll, Question, Choice, Vote, User
from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

class PollResultTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.poll = Poll.objects.create(
            title="Election",
            expiry=timezone.now() + timedelta(days=1),
            user=self.user  # <-- FIX HERE
        )

        self.question = self.poll.questions.create(text="Who should win?")
        self.choice1 = self.question.choices.create(text="Candidate A")
        self.choice2 = self.question.choices.create(text="Candidate B")
        self.choice3 = self.question.choices.create(text="Candidate C")

        Vote.objects.bulk_create([
            Vote(question=self.question, choice=self.choice1, ip_address='1.1.1.1'),
            Vote(question=self.question, choice=self.choice1, ip_address='1.1.1.2'),
            Vote(question=self.question, choice=self.choice2, ip_address='1.1.1.3'),
        ])

        self.client = APIClient()

    def test_poll_results(self):
        url = reverse('poll-results', args=[self.poll.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data['poll'], self.poll.title)
        self.assertEqual(len(data['results']), 1)
        result = data['results'][0]
        self.assertEqual(result['question'], self.question.text)
        self.assertEqual(result['winner']['choice'], self.choice1.text)
        self.assertEqual(result['winner']['votes'], 2)
