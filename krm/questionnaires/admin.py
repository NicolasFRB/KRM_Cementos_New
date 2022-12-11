# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe

# from tinymce.models import HTMLField

from django.forms import ModelForm
from django import forms

from krm.questionnaires.models import (
    Questionnaire,
    Question,
    QuestionTest,
    EvaluationQuestionnaire,
    Scope
)


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    model = Questionnaire
    list_display = ('ref', 'name',)


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    model = Scope
    list_display = ('ref', 'name', 'questionnaire', )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ('ref', 'title', )
    list_filter = ('scopes__questionnaire', 'scopes')


@admin.register(QuestionTest)
class QuestionTestAdmin(admin.ModelAdmin):
    model = QuestionTest
    list_display = ('pk', 'evaluation', 'evaluator',
                    'question', 'status')


@admin.register(EvaluationQuestionnaire)
class EvaluationQuestionnaireAdmin(admin.ModelAdmin):
    model = EvaluationQuestionnaire
    list_display = ('ref', 'questionnaire', 'status',)
