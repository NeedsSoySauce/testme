import random

from django.test import TestCase
from django.urls import reverse

from quizzes import INDEX_LATEST_QUIZ_COUNT, NO_QUIZZES_AVAILABLE_MESSAGE
from quizzes.tests import create_quizzes, create_quiz, create_populated_question


class QuizzesIndexTests(TestCase):
    def test_no_quizzes(self):
        """ The correct message is displayed if no quizzes are available. """
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, NO_QUIZZES_AVAILABLE_MESSAGE)
        self.assertQuerysetEqual(response.context['quizzes'], [])

    def test_latest_quizzes_are_displayed_with_less_than_max(self):
        """ The most recently created quizzes are displayed when there's less than the maximum amount. """
        objects = create_quizzes(INDEX_LATEST_QUIZ_COUNT - 1)
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['quizzes'], [repr(obj) for obj in objects])

    def test_latest_quizzes_are_displayed_with_max(self):
        """ The most recently created quizzes are displayed when there's exactly the maximum amount. """
        objects = create_quizzes(INDEX_LATEST_QUIZ_COUNT)
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['quizzes'], [repr(obj) for obj in objects])

    def test_latest_quizzes_are_displayed_with_more_than_max(self):
        """ The most recently created quizzes are displayed when there's more than the maximum amount. """
        objects = create_quizzes(INDEX_LATEST_QUIZ_COUNT + 1)
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['quizzes'], [repr(obj) for obj in objects])


class QuizzesQuizAttemptTests(TestCase):
    def setUp(self) -> None:
        self.quiz = create_quiz()

        # Create two questions, the second of which is multiple choice
        self.q1 = create_populated_question([True, False], 'Question 1')
        self.q2 = create_populated_question([True, True, False], ' Question 2')

        self.quiz.questions.add(self.q1, self.q2)
        self.quiz.save()

        self.q1_answer_ids = list(self.q1.answer_set.all().filter(is_correct_answer=True).values_list('pk', flat=True))
        self.q2_answer_ids = list(self.q2.answer_set.all().filter(is_correct_answer=True).values_list('pk', flat=True))

        # Questions are shuffled, so to we need to set a seed to create consistent results.
        # This seed will result in question 1 and then question 2 being shown.
        random.seed(123)

    def test_quiz_attempt(self):
        url_kwargs = {'quiz_id': self.quiz.pk}
        url = reverse('quizzes:quiz', kwargs=url_kwargs)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.csrf_cookie_set)
        self.assertContains(response, 'Question 1', html=True)

        response = self.client.post(url, data={'answers': self.q1_answer_ids}, follow=True)
        self.assertRedirects(response, url)
        self.assertTrue(response.csrf_cookie_set)
        self.assertContains(response, 'Question 2', html=True)

        response = self.client.post(url, data={'answers': self.q2_answer_ids}, follow=True)
        self.assertRedirects(response, reverse('quizzes:results', kwargs=url_kwargs))
        self.assertContains(response, 'Results', html=True)
        self.assertContains(response, '2 / 2')  # html = False here as we only want a character-by-character match
