from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

import quizzes
from .models import Quiz


def index(request):
    context = {
        'quizzes': Quiz.objects.order_by('-created_on')[:quizzes.INDEX_LATEST_QUIZ_COUNT],
        'no_quizzes_message': quizzes.NO_QUIZZES_AVAILABLE_MESSAGE
    }
    return render(request, 'quizzes/index.html', context)
