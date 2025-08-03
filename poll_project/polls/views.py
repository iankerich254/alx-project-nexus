from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Poll, Question, Choice, Vote
from .serializers import PollSerializer, QuestionSerializer, ChoiceSerializer, VoteSerializer

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="List all polls",
        operation_description="Returns a list of all polls.",
        responses={200: PollSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a poll",
        operation_description="Returns detailed information about a single poll.",
        responses={200: PollSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new poll",
        operation_description="Creates a poll. Expiry date must be in the future.",
        responses={201: PollSerializer(), 400: "Validation Error"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a poll",
        operation_description="Updates the title, expiry, or other fields of a poll.",
        responses={200: PollSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a poll",
        operation_description="Deletes a poll by ID.",
        responses={204: "Poll deleted"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        expiry = serializer.validated_data.get('expiry')
        if expiry and expiry < timezone.now():
            raise ValidationError("Expiry date must be in the future.")
        serializer.save(user=self.request.user)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="List all questions")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a question")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a question")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update a question")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a question")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="List all choices")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a choice")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a choice")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update a choice")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a choice")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class VoteAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Submit a vote for a specific question",
        operation_description="Allows an anonymous or authenticated user to vote for a choice in a poll question. Prevents duplicate votes from the same session or IP.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['choice'],
            properties={
                'choice': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the selected choice'
                )
            }
        ),
        responses={
            201: openapi.Response(description="Vote submitted successfully"),
            400: openapi.Response(description="Invalid request or duplicate vote")
        }
    )
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
    @swagger_auto_schema(
        operation_summary="Get poll results with winners",
        operation_description="Returns vote counts and winners for each question in a poll.",
        responses={
            200: openapi.Response(
                description="Poll results returned successfully",
                examples={
                    "application/json": {
                        "poll": "Your Favorite Programming Language",
                        "results": [
                            {
                                "question": "Which language do you prefer?",
                                "choices": [
                                    {"choice": "Python", "votes": 10},
                                    {"choice": "JavaScript", "votes": 5}
                                ],
                                "winner": {"choice": "Python", "votes": 10}
                            }
                        ]
                    }
                }
            ),
            404: openapi.Response(description="Poll not found")
        }
    )
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