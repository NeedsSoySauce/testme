from django.contrib import admin

from .models import Tag, Question, Answer, Quiz


class TagInLine(admin.TabularInline):
    model = Question.tags.through
    extra = 1
    classes = ['collapse']
    verbose_name_plural = 'Tags'


class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 1
    classes = ['collapse']
    readonly_fields = ('votes',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [TagInLine]
    search_fields = ['tag_name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    exclude = ('tags',)
    readonly_fields = ('created_on', 'updated_on')
    fieldsets = [
        (None, {'fields': ['created_on', 'updated_on', 'question_text', 'description']})
    ]
    inlines = [AnswerInLine, TagInLine]
    list_display = ('question_text', 'created_on', 'updated_on')
    list_filter = ['created_on', 'tags']
    search_fields = ['question_text', 'tags__tag_name', 'description']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['answer_text']
    readonly_fields = ('votes',)


class QuestionInLine(admin.TabularInline):
    model = Quiz.questions.through
    extra = 1
    classes = ['collapse']
    verbose_name_plural = 'Questions'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    exclude = ('questions',)
    readonly_fields = ('created_on', 'updated_on')
    fieldsets = [
        (None, {'fields': ['created_on', 'updated_on', 'quiz_name', 'description']})
    ]
    inlines = [QuestionInLine]
    list_display = ('quiz_name', 'created_on', 'updated_on')
    list_filter = ['created_on', 'questions__tags']
    search_fields = ['quiz_name', 'description', 'questions__question_text']
