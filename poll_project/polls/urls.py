from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PollViewSet, QuestionViewSet, ChoiceViewSet, VoteAPIView, PollResultsAPIView

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'choices', ChoiceViewSet, basename='choice')


urlpatterns = router.urls + [
    path('questions/<int:question_id>/vote/', VoteAPIView.as_view(), name='vote'),
    path('polls/<int:pk>/vote/', VoteAPIView.as_view(), name='vote'),
    path('polls/<int:pk>/results/', PollResultsAPIView.as_view(), name='poll-results'),
]
