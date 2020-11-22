from rest_framework import routers

from . import views

app_name = 'quizzes'

router = routers.DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'quizzes', views.QuizViewSet)
