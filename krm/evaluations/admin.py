from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

# Register your models here.
from krm.evaluations.models import (
    Evaluation,
    ControlTest,
    ControlTestAnswer,
    RemediationPlan
)


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    model = Evaluation
    list_display = ('ref', 'status', 'date_begin')
    list_filter = ('status',)


@admin.register(ControlTest)
class ControlTestAdmin(admin.ModelAdmin):
    model = ControlTest
    list_display = ('evaluation', 'control', 'identifier', 'status')
    list_filter = ('status', 'evaluation__company', 'evaluation')


@admin.register(ControlTestAnswer)
class ControlTestAnswerAdmin(admin.ModelAdmin):
    model = ControlTestAnswer
    list_display = ('control_test', 'user', 'created')
    list_filter = ('control_test__evaluation',)


@admin.register(RemediationPlan)
class RemediationPlanAdmin(admin.ModelAdmin):
    model = RemediationPlan
    list_display = ('control_test', 'created', 'modified')
    readonly_fields = ('created', 'modified')
