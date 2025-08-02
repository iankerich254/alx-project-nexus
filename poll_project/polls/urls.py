from rest_framework.routers import DefaultRouter
from .views import PollViewSet, QuestionViewSet, ChoiceViewSet

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'choices', ChoiceViewSet, basename='choice')


urlpatterns = router.urls
