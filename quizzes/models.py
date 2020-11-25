from django.contrib.sessions.models import Session
from django.db import models

from testme.settings import AUTH_USER_MODEL


class AbstractTimestampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Question(AbstractTimestampedModel):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=255)
    description = models.TextField(help_text="Any additional details related to this question", blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.text

    def is_multiple_choice(self) -> bool:
        """
        Returns True if this question is multiple choice (a question is multiple choice if it has multiple correct answers.
        """
        return self.answers.filter(is_correct_answer=True).count() > 1


class Answer(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0, editable=False, help_text="Number of times this answer has been chosen.")
    is_correct_answer = models.BooleanField(default=False, help_text="Whether or not this answer is correct.")

    def __str__(self):
        return self.text


class Quiz(AbstractTimestampedModel):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(help_text="Any additional details related to this quiz", blank=True)
    questions = models.ManyToManyField(Question)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.name
