import datetime
from typing import List
from unittest import mock

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from quizzes import INDEX_LATEST_QUIZ_COUNT
from quizzes.models import Quiz, Answer, Question, Tag


def create_tag(name='tag'):
    return Tag.objects.create(name=name or 'tag')


def create_question(question_text: str = 'question'):
    return Question.objects.create(text=question_text or 'question')


def create_answer(question: Question, is_correct_answer: bool, creator = None):
    return Answer.objects.create(question=question, text='answer', is_correct_answer=is_correct_answer, creator=creator)


def create_quizzes(number_of_quizzes=1):
    _ = [Quiz.objects.create(name=f'quiz_{i}') for i in range(number_of_quizzes)]
    return Quiz.objects.order_by('-created_on')[:INDEX_LATEST_QUIZ_COUNT]


def create_quiz():
    return create_quizzes()[0]


def create_populated_question(answer_states: List[bool], question_text: str = None):
    """
    Creates a question with answers using the given data.

    e.g. if answers = [True, False] one correct and one incorrect answer will be created.
    """
    question = create_question(question_text)

    for state in answer_states:
        create_answer(question, state)

    return question


def create_api_response(status_code: int = 200, message: str = "OK", data=None):
    response = {
        "status": status_code,
        "success": status_code < 400,
        "message": message,
        'data': data
    }

    return response


class MockedTestCase(TestCase):
    """ Overrides the behaviour of django's automatic timestamps, e.g. auto_now_add. """

    def run(self, result=None):
        mocked = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            super().run(result)


class UserAuthTestsMixin:
    """ Adds a 'setUpTestUsers' method to create """

    def setUpTestUsers(self) -> None:
        """
        Creates two regular users '.user' and '.other'; an admin user '.admin'; and an anonymous user '.anonymous'.
        """
        self.password = "thisisasecret"
        self.other = get_user_model().objects.create_user("other", password=self.password)
        self.user = get_user_model().objects.create_user("user", password=self.password)
        self.admin = get_user_model().objects.create_superuser("admin", password=self.password)
        self.anonymous = AnonymousUser()
