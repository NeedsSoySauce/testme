from typing import List

from django.test import TestCase
from django.urls import reverse

import quizzes
from .models import Quiz


def create_quizzes(number_of_quizzes=1):
    _ = [Quiz.objects.create(quiz_name=f'quiz_{i}') for i in range(number_of_quizzes)]
    return Quiz.objects.order_by('-created_on')[:quizzes.INDEX_LATEST_QUIZ_COUNT]


class QuizzesIndexTests(TestCase):
    def test_no_quizzes(self):
        """ The correct message is displayed if no quizzes are available. """
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, quizzes.NO_QUIZZES_AVAILABLE_MESSAGE)
        self.assertQuerysetEqual(response.context['quizzes'], [])

    def test_latest_quizzes_are_displayed_with_less_than_max(self):
        """ The most recently created quizzes are displayed when there's less than the maximum amount. """
        objects = create_quizzes(quizzes.INDEX_LATEST_QUIZ_COUNT - 1)
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['quizzes'], [repr(obj) for obj in objects])

    def test_latest_quizzes_are_displayed_with_max(self):
        """ The most recently created quizzes are displayed when there's exactly the maximum amount. """
        objects = create_quizzes(quizzes.INDEX_LATEST_QUIZ_COUNT)
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['quizzes'], [repr(obj) for obj in objects])

    def test_latest_quizzes_are_displayed_with_more_than_max(self):
        """ The most recently created quizzes are displayed when there's more than the maximum amount. """
        objects = create_quizzes(quizzes.INDEX_LATEST_QUIZ_COUNT + 1)
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['quizzes'], [repr(obj) for obj in objects])
