import random
from typing import List

from django.test import TestCase
from django.urls import reverse

from quizzes import INDEX_LATEST_QUIZ_COUNT, NO_QUIZZES_AVAILABLE_MESSAGE
from quizzes.forms import QuestionForm
from quizzes.models import Quiz, QuizQuestionResponseAnswer, QuizAttempt, QuizQuestionResponse, Question, Answer


def create_question(question_text: str = None):
    return Question.objects.create(question_text=question_text or 'question')


def create_answer(question: Question, is_correct_answer: bool):
    return Answer.objects.create(question=question, answer_text='answer', is_correct_answer=is_correct_answer)


def create_quizzes(number_of_quizzes=1):
    _ = [Quiz.objects.create(quiz_name=f'quiz_{i}') for i in range(number_of_quizzes)]
    return Quiz.objects.order_by('-created_on')[:INDEX_LATEST_QUIZ_COUNT]


def create_quiz():
    return create_quizzes()[0]


def create_quiz_attempt(session_key: str, quiz: Quiz, active_question: Question = None):
    return QuizAttempt.objects.create(session_key=session_key, quiz=quiz, active_question=active_question)


def create_quiz_question_response(quiz_attempt: QuizAttempt, question: Question):
    return QuizQuestionResponse.objects.create(quiz_attempt=quiz_attempt, question=question)


def create_quiz_question_response_answer(quiz_question_response: QuizQuestionResponse, answer: Answer):
    return QuizQuestionResponseAnswer.objects.create(quiz_question_response=quiz_question_response, answer=answer)


def create_populated_quiz_question_response(answer_states: List[bool],
                                            quiz_attempt: QuizAttempt = None,
                                            quiz: Quiz = None):
    """
    Creates a quiz question response with the selected answers matching the given states.

    e.g. if answer_states = [True, False] one correct answer and one incorrect answer will be created.
    """
    question = create_question()
    quiz = quiz or create_quiz()
    quiz.questions.add(question)
    quiz_attempt = quiz_attempt or create_quiz_attempt('abc', quiz, question)
    quiz_question_response = create_quiz_question_response(quiz_attempt, question)

    for state in answer_states:
        answer = create_answer(question, state)
        create_quiz_question_response_answer(quiz_question_response, answer)

    return quiz_question_response


def create_populated_quiz_attempt(response_states: List[bool]):
    """
    Creates a quiz attempt with question responses matching the given states.

    e.g. if response_states = [True, False] one correct response and one incorrect response will be created.
    """
    question = create_question()
    quiz = create_quiz()
    quiz_attempt = create_quiz_attempt('abc', quiz, question)

    for state in response_states:
        create_populated_quiz_question_response([state], quiz_attempt, quiz)

    return quiz_attempt


def create_populated_question(answer_states: List[bool], question_text: str = None):
    """
    Creates a question with answers using the given data.

    e.g. if answers = [True, False] one correct and one incorrect answer will be created.
    """
    question = create_question(question_text)

    for state in answer_states:
        create_answer(question, state)

    return question


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


class QuestionFormTests(TestCase):
    def setUp(self):
        self.choices = [(i, f'answer_{i}') for i in range(4)]

    def test_renders_checkboxes_when_multiple_choice(self):
        """ When multi is True answers are rendered as multiple choice checkboxes. """
        form = QuestionForm(choices=self.choices, multi=True)
        self.assertIn('checkbox', str(form))

    def test_renders_radio_buttons_when_not_multiple_choice(self):
        form = QuestionForm(choices=self.choices, multi=False)
        self.assertIn('radio', str(form))

    def test_cleaned_answers_is_always_list(self):
        data = {"answers": [choice[0] for choice in self.choices]}

        form = QuestionForm(data=data, choices=self.choices, multi=True)
        form.full_clean()
        answers = form.cleaned_data['answers']
        self.assertIsInstance(answers, list)

        data = {"answers": self.choices[0][0]}
        form = QuestionForm(data=data, choices=self.choices, multi=False)
        form.full_clean()
        answers = form.cleaned_data['answers']
        self.assertIsInstance(answers, list)
