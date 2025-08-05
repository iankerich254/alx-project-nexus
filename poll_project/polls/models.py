from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Enforces unique email and username.
    """
    id = models.AutoField(primary_key=True)  # Explicit PK
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Poll(models.Model):
    """
    Poll model representing a survey or voting topic.
    Related to the user who created it and has an expiry date.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')  # FK to User
    expiry = models.DateTimeField()

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Question model representing a question under a specific poll.
    Each poll can have multiple questions.
    """
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')  # FK to Poll

    def __str__(self):
        return self.text


class Choice(models.Model):
    """
    Choice model representing answer options for a question.
    Each question can have multiple choices.
    """
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')  # FK to Question

    def __str__(self):
        return self.text


class Vote(models.Model):
    """
    Vote model for storing individual user or anonymous votes.
    Tracks by user, IP address, and session to prevent duplicate votes.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes', null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'question'),
            ('ip_address', 'question'),
            ('session_key', 'question'),
        ]

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} voted {self.choice.text}"
