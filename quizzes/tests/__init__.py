from typing import List

from quizzes import INDEX_LATEST_QUIZ_COUNT
from quizzes.models import QuizAttempt, QuizQuestionResponse, QuizQuestionResponseAnswer, Quiz, Answer, Question


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
