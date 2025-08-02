from rest_framework import serializers
from django.db import models
from .models import Poll, Question, Choice, Vote

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'question']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'poll', 'choices']

class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'created_at', 'updated_at', 'user', 'expiry', 'questions']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'choice']

    def validate(self, data):
        request = self.context['request']
        choice = data['choice']
        question = choice.question

        ip_address = self._get_ip(request)
        session_key = request.session.session_key

        # Ensure session key is set
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        # Duplicate vote check (by IP or session)
        existing_vote = Vote.objects.filter(
            question=question
        ).filter(
            models.Q(ip_address=ip_address) | models.Q(session_key=session_key)
        ).exists()

        if existing_vote:
            raise serializers.ValidationError("Duplicate vote detected for this question.")

        return data

    def _get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip