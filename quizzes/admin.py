from django.contrib import admin

from .models import Tag, Question, Answer, Quiz


class TagInLine(admin.TabularInline):
    model = Question.tags.through
    extra = 1
    classes = ['collapse']
    verbose_name_plural = 'Tags'


class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 3
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
        (None, {'fields': ['created_on', 'updated_on', 'text', 'description']})
    ]
    inlines = [AnswerInLine, TagInLine]
    list_display = ('text', 'created_on', 'updated_on')
    list_filter = ['created_on', 'tags']
    search_fields = ['text', 'tags__name', 'description']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ('votes',)


class QuestionInLine(admin.TabularInline):
    model = Quiz.questions.through
    extra = 3
    classes = ['collapse']
    verbose_name_plural = 'Questions'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    exclude = ('questions',)
    readonly_fields = ('created_on', 'updated_on')
    fieldsets = [
        (None, {'fields': ['created_on', 'updated_on', 'name', 'description']})
    ]
    inlines = [QuestionInLine]
    list_display = ('name', 'created_on', 'updated_on')
    list_filter = ['created_on', 'questions__tags']
    search_fields = ['name', 'description', 'questions__text']
