from django.test import TestCase

from quizzes.tests import create_populated_quiz_question_response, create_populated_quiz_attempt, \
    create_populated_question


class QuizQuestionResponseModelTests(TestCase):
    def test_is_correct_when_correct(self):
        """ Returns True when the correct answer is selected. """
        quiz_question_response = create_populated_quiz_question_response([True])
        self.assertTrue(quiz_question_response.is_correct())

    def test_is_correct_when_incorrect(self):
        """ Returns False when the incorrect answer is selected. """
        quiz_question_response = create_populated_quiz_question_response([False])
        self.assertFalse(quiz_question_response.is_correct())


class QuizAttemptModelTests(TestCase):
    def test_score_when_zero(self):
        """ Score equals zero when there are no correct responses. """
        quiz_attempt = create_populated_quiz_attempt([False])
        self.assertEquals(quiz_attempt.score(), 0)

    def test_score_when_between_zero_and_max(self):
        """ Scores is correct when the number of correct responses is greater than zero but less than the max score """
        quiz_attempt = create_populated_quiz_attempt([True, True, False])
        self.assertEquals(quiz_attempt.score(), 2)

    def test_score_when_max(self):
        """ Score equals the max score when all responses are correct. """
        quiz_attempt = create_populated_quiz_attempt([True])
        self.assertEquals(quiz_attempt.score(), 1)

    def test_max_score_when_zero(self):
        """ Max score equals zero when there are no questions with correct responses. """
        quiz_attempt = create_populated_quiz_attempt([])
        self.assertEquals(quiz_attempt.max_score(), 0)

    def test_max_score_when_non_zero(self):
        """ Max score equals the number of questions when there are questions. """
        quiz_attempt = create_populated_quiz_attempt([False])
        self.assertEquals(quiz_attempt.max_score(), 1)


class QuestionModelTests(TestCase):
    def test_is_multiple_choice_when_true(self):
        """ Returns True when a question has more than one correct answer. """
        question = create_populated_question([True, True])
        self.assertTrue(question.is_multiple_choice())

    def test_is_multiple_choice_when_false(self):
        """ Returns False when a question has one correct answer. """
        question = create_populated_question([True])
        self.assertFalse(question.is_multiple_choice())
