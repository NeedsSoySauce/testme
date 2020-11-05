from django.urls import path

from . import views

app_name = 'quizzes'
urlpatterns = [
    path('', views.index, name='index'),
    path('quizzes/<int:quiz_id>', views.quizzes, name='quiz'),
    path('quizzes/<int:quiz_id>/results', views.results, name='results')
]
