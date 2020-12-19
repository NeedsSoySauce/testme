from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Quiz, Question, Answer, Tag
from .permissions import IsCreatorOrAdminUserOrReadOnly
from .serializers import TagSerializer, QuestionSerializer, AnswerSerializer, QuizSerializer
from .viewsets import UserLinkedModelViewSet


class TagViewSet(ModelViewSet):
    """ Allows tags to be viewed or edited. """
    queryset = Tag.objects.all().order_by('pk')
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class QuestionViewSet(UserLinkedModelViewSet):
    """ Allows questions to be viewed or edited. """
    queryset = Question.objects.all().order_by('pk')
    serializer_class = QuestionSerializer
    permission_classes = [IsCreatorOrAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['creator__username', 'creator__email', 'text', 'description', 'tags__name']


class AnswerViewSet(UserLinkedModelViewSet):
    """ Allows answers to be viewed or edited. """
    queryset = Answer.objects.all().order_by('pk')
    serializer_class = AnswerSerializer
    permission_classes = [IsCreatorOrAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['creator__username', 'creator__email', 'question__text', 'question__description',
                     'question__tags__name', 'text']


class QuizViewSet(UserLinkedModelViewSet):
    """ Allows quizzes to be viewed or edited. """
    queryset = Quiz.objects.all().order_by('pk')
    serializer_class = QuizSerializer
    permission_classes = [IsCreatorOrAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['creator__username', 'creator__email', 'name', 'description', 'questions__text',
                     'questions__description', 'questions__tags__name']
