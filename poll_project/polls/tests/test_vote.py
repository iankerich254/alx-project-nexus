from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from polls.models import User, Poll, Question, Choice, Vote

User = get_user_model()

class VoteTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create user (though not used for anonymous voting)
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='pass1234')

        # Create poll
        self.poll = Poll.objects.create(
            title="Favorite Programming Language?",
            user=self.user,
            expiry=timezone.now() + timedelta(days=1)
        )

        # Create question
        self.question = Question.objects.create(text="What's your favorite language?", poll=self.poll)

        # Create choices
        self.choice1 = Choice.objects.create(text="Python", question=self.question)
        self.choice2 = Choice.objects.create(text="JavaScript", question=self.question)

        # Set vote endpoint URL
        self.vote_url = f"/api/questions/{self.question.id}/vote/"

    def test_vote_success(self):
        response = self.client.post(
            self.vote_url,
            {'choice': self.choice1.id},
            REMOTE_ADDR='127.0.0.1',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.first().choice, self.choice1)

    def test_duplicate_vote_same_ip(self):
        # First vote
        self.client.post(
            self.vote_url,
            {'choice': self.choice1.id},
            REMOTE_ADDR='127.0.0.1',
            content_type='application/json'
        )
        # Duplicate vote
        response = self.client.post(
            self.vote_url,
            {'choice': self.choice2.id},
            REMOTE_ADDR='127.0.0.1',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"You have already voted from this IP", response.content)

    def test_duplicate_vote_same_session(self):
        session = self.client.session
        session[f'has_voted_question_{self.question.id}'] = True
        session.save()

        response = self.client.post(
            self.vote_url,
            {'choice': self.choice2.id},
            REMOTE_ADDR='192.168.1.10',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"You have already voted in this session", response.content)

    def test_vote_expired_poll(self):
        self.poll.expiry = timezone.now() - timedelta(days=1)
        self.poll.save()

        response = self.client.post(
            self.vote_url,
            {'choice': self.choice1.id},
            REMOTE_ADDR='127.0.0.1',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"This poll has expired", response.content)

class PollResultsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        
        self.poll = Poll.objects.create(
            title="Test Poll",
            expiry=timezone.now() + timedelta(days=7),
            user=self.user
        )
        self.question = Question.objects.create(poll=self.poll, text="Q1?")
        self.choice1 = Choice.objects.create(question=self.question, text="A")
        self.choice2 = Choice.objects.create(question=self.question, text="B")
        Vote.objects.create(choice=self.choice1, ip_address="1.1.1.1")
        Vote.objects.create(choice=self.choice1, ip_address="1.1.1.2")
        Vote.objects.create(choice=self.choice2, ip_address="1.1.1.3")

    def test_result_counts(self):
        url = f"/api/polls/{self.poll.id}/results/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["poll"], self.poll.title)
        self.assertEqual(response.data["results"][0]["choices"][0]["votes"], 2)  # choice1
        self.assertEqual(response.data["results"][0]["choices"][1]["votes"], 1)  # choice2