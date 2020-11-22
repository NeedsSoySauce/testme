from django.test import TestCase

from quizzes.tests import create_populated_question


class QuestionModelTests(TestCase):
    def test_is_multiple_choice_when_true(self):
        """ Returns True when a question has more than one correct answer. """
        question = create_populated_question([True, True])
        self.assertTrue(question.is_multiple_choice())

    def test_is_multiple_choice_when_false(self):
        """ Returns False when a question has one correct answer. """
        question = create_populated_question([True])
        self.assertFalse(question.is_multiple_choice())
