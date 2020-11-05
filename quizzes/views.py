import random

from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_safe

from . import INDEX_LATEST_QUIZ_COUNT, NO_QUIZZES_AVAILABLE_MESSAGE
from .forms import QuestionForm
from .models import Quiz, Question, QuizAttempt, Answer, QuizQuestionResponse, QuizQuestionResponseAnswer


@require_safe
def index(request):
    context = {
        'quizzes': Quiz.objects.order_by('-created_on')[:INDEX_LATEST_QUIZ_COUNT],
        'no_quizzes_message': NO_QUIZZES_AVAILABLE_MESSAGE
    }
    return render(request, 'quizzes/index.html', context)


@require_http_methods(["GET", "HEAD", "POST"])
def quizzes(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # Client may not have a session if this is their first request
    # TODO - handle clients which have cookies disabled/blocked or don't support cookies
    if not request.session.exists(request.session.session_key):
        request.session.create()

    # Create a quiz attempt or retrieve the last one based on the quiz and session
    quiz_attempt, is_created = QuizAttempt.objects.get_or_create(quiz=quiz,
                                                                 session_key=request.session.session_key,
                                                                 state=QuizAttempt.State.IN_PROGRESS)

    # Retrieve all question ids and shuffle them based on this quiz attempt's seed (so the order remains constant)
    question_ids = [q.pk for q in quiz.questions.all()]
    random.seed(quiz_attempt.seed)
    random.shuffle(question_ids)

    # Check if a quiz attempt was created or we're resuming a previous one
    if is_created:
        question = Question.objects.get(pk=question_ids[0])
        quiz_attempt.active_question = question
        quiz_attempt.save()
    else:
        # Get the ids of questions the client has already responded to
        answered = quiz_attempt.quizquestionresponse_set.values('pk')

        if answered:
            # TODO handle case where active question is deleted
            # can probably be done by just finding the id of the next question that hasn't been complete
            question = Question.objects.get(pk=quiz_attempt.active_question_id)
        else:
            question = Question.objects.get(pk=question_ids[0])

    # TODO prevent a client changing a question they've already answered while a quiz is in-progress

    is_multiple_choice = question.is_multiple_choice()

    # Create choices for question forms
    choices = tuple((answer.id, answer.answer_text) for answer in question.answer_set.all())

    if request.method == 'POST':
        form = QuestionForm(request.POST, choices=choices, multi=is_multiple_choice)
        if form.is_valid():
            # Update quiz attempt
            answer_ids = form.cleaned_data['answers']

            # We need to save the response to the current question but also update the active_question_id

            # Select the id following the one the client gave
            next_index = question_ids.index(question.pk) + 1
            is_last_question = next_index >= len(question_ids)
            next_question = None if is_last_question else Question.objects.get(pk=question_ids[next_index])

            # - Save the response to the current question
            # - Update the active question to point to the next question or null if there isn't another question
            with transaction.atomic():
                quiz_response = QuizQuestionResponse.objects.create(quiz_attempt=quiz_attempt, question=question)
                quiz_response.save()

                answers = Answer.objects.filter(pk__in=answer_ids).all()
                for answer in answers:
                    QuizQuestionResponseAnswer.objects.create(quiz_question_response=quiz_response, answer=answer)

                quiz_attempt.quizquestionresponse_set.add(quiz_response)
                quiz_attempt.active_question = next_question

                if next_question is None:
                    quiz_attempt.state = QuizAttempt.State.COMPLETE

                quiz_attempt.save()

            # Redirect user to the next question or, if they've answered every question, redirect them to their results
            if is_last_question:
                return redirect('quizzes:results', quiz_id=quiz_id)

            return redirect('quizzes:quiz', quiz_id=quiz_id)
    else:
        form = QuestionForm(choices=choices, multi=is_multiple_choice)

    context = {
        'quiz': quiz,
        'question': question,
        'form': form
    }

    return render(request, 'quizzes/question.html', context)


@require_safe
def results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    quiz_attempts = QuizAttempt.objects.filter(session_key=request.session.session_key).order_by("-updated_on")

    context = {
        'quiz': quiz,
        'quiz_attempts': quiz_attempts
    }

    return render(request, 'quizzes/results.html', context)
