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


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0, editable=False, help_text="Number of times this answer has been chosen.")
    is_correct_answer = models.BooleanField(default=False, help_text="Whether or not this answer is correct.")

    def __str__(self):
        return self.answer_text


class Quiz(AbstractTimestampedModel):
    class Meta:
        verbose_name = 'Quizzes'

    quiz_name = models.CharField(max_length=255)
    description = models.TextField(help_text="Any additional details related to this quiz", blank=True)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.quiz_name
