from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Count

from .models import Poll, Question, Choice, Vote
from .serializers import PollSerializer, QuestionSerializer, ChoiceSerializer, VoteSerializer

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        expiry = serializer.validated_data.get('expiry')
        if expiry and expiry < timezone.now():
            raise ValidationError("Expiry date must be in the future.")
        serializer.save(user=self.request.user)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VoteAPIView(APIView):
    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        poll = question.poll

        # Check if poll expired
        if poll.expiry and poll.expiry < timezone.now():
            return Response({"error": "This poll has expired."}, status=status.HTTP_400_BAD_REQUEST)

        # IP detection
        ip_address = request.META.get('REMOTE_ADDR')
        if Vote.objects.filter(question=question, ip_address=ip_address).exists():
            return Response({"error": "You have already voted from this IP."}, status=status.HTTP_400_BAD_REQUEST)

        # Session detection
        session_key = f"has_voted_question_{question.id}"
        if request.session.get(session_key):
            return Response({"error": "You have already voted in this session."}, status=status.HTTP_400_BAD_REQUEST)

        choice_id = request.data.get("choice")
        choice = get_object_or_404(Choice, id=choice_id, question=question)

        Vote.objects.create(
            question=question,
            choice=choice,
            ip_address=ip_address
        )
        request.session[session_key] = True  # Set session flag

        return Response({"message": "Vote submitted successfully."}, status=status.HTTP_201_CREATED)

class PollResultsAPIView(APIView):
    def get(self, request, pk):
        try:
            poll = Poll.objects.prefetch_related('questions__choices__votes').get(pk=pk)
        except Poll.DoesNotExist:
            return Response({"detail": "Poll not found."}, status=status.HTTP_404_NOT_FOUND)

        results = []
        for question in poll.questions.all():
            choices = question.choices.annotate(vote_count=Count('votes')).order_by('-vote_count')
            winner = choices.first()

            results.append({
                "question": question.text,
                "choices": [
                    {"choice": c.text, "votes": c.vote_count}
                    for c in choices
                ],
                "winner": {
                    "choice": winner.text,
                    "votes": winner.vote_count
                } if winner else None
            })

        return Response({
            "poll": poll.title,
            "results": results
        })