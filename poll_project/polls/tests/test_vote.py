from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta

from polls.models import User, Poll, Question, Choice, Vote

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
