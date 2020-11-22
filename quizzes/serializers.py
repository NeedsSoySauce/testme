from rest_framework import serializers

from quizzes.models import Tag, Question, Answer, Quiz


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    question = serializers.HyperlinkedRelatedField(queryset=Question.objects.all(), view_name='question-detail')

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    is_multiple_choice = serializers.ReadOnlyField()
    answers = serializers.HyperlinkedRelatedField(queryset=Answer.objects.all(), view_name='answer-detail', many=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.HyperlinkedRelatedField(many=True, queryset=Question.objects.all(),
                                                    view_name='question-detail')

    class Meta:
        model = Quiz
        fields = '__all__'
