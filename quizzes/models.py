import random

from django.contrib.sessions.models import Session
from django.db import models


class AbstractTimestampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    tag_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tag_name


class Question(AbstractTimestampedModel):
    question_text = models.CharField(max_length=255)
    description = models.TextField(help_text="Any additional details related to this question", blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.question_text

    def is_multiple_choice(self) -> bool:
        """
        Returns True if this question is multiple choice (a question is multiple choice if it has multiple correct answers.
        """
        return self.answer_set.filter(is_correct_answer=True).count() > 1


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0, editable=False, help_text="Number of times this answer has been chosen.")
    is_correct_answer = models.BooleanField(default=False, help_text="Whether or not this answer is correct.")

    def __str__(self):
        return self.answer_text


class Quiz(AbstractTimestampedModel):
    quiz_name = models.CharField(max_length=255)
    description = models.TextField(help_text="Any additional details related to this quiz", blank=True)
    questions = models.ManyToManyField(Question)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.quiz_name


def _randint() -> int:
    """ Returns a random integer between 0 and 2,000,000. """
    return random.randint(0, 2000000)


class QuizAttempt(AbstractTimestampedModel):
    class State(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS'
        COMPLETE = 'COMPLETE'

    session_key = models.CharField(max_length=40)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    seed = models.IntegerField(default=_randint)
    state = models.CharField(max_length=255,
                             choices=State.choices,
                             default=State.IN_PROGRESS)
    active_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)

    def score(self) -> int:
        """ Returns the score for this quiz which is equal to number of correct responses. """
        return sum(response.is_correct() for response in self.quizquestionresponse_set.all())

    def max_score(self) -> int:
        """ Returns the maximum possible score for this quiz which is equal to the number of questions in this quiz. """
        return self.quiz.questions.count()


class QuizQuestionResponse(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answers = models.ManyToManyField(Answer, through='QuizQuestionResponseAnswer')

    def is_correct(self) -> bool:
        """ Returns True if this question's response is correct, otherwise returns False. """
        correct_answer_ids = self.question.answer_set.filter(is_correct_answer=True).values_list('pk', flat=True)
        answer_ids = self.answers.values_list('pk', flat=True)
        return set(correct_answer_ids) == set(answer_ids)


class QuizQuestionResponseAnswer(models.Model):
    quiz_question_response = models.ForeignKey(QuizQuestionResponse, on_delete=models.PROTECT)
    answer = models.ForeignKey(Answer, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['quiz_question_response', 'answer'], name='unique_answer')
        ]
