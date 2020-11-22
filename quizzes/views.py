from rest_framework import viewsets

from .models import Quiz, Question, Answer, Tag
from .serializers import TagSerializer, QuestionSerializer, AnswerSerializer, QuizSerializer


class TagViewSet(viewsets.ModelViewSet):
    """ Allows tags to be viewed or edited. """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """ Allows questions to be viewed or edited. """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """ Allows answers to be viewed or edited. """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class QuizViewSet(viewsets.ModelViewSet):
    """ Allows quizzes to be viewed or edited. """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
