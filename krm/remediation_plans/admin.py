from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

# Register your models here.
from krm.remediation_plans.models import (
    RemediationPlan,
    RemediationPlanAnswer
)


@admin.register(RemediationPlan)
class RemediationPlanAdmin(admin.ModelAdmin):
    model = RemediationPlan
    list_display = ('pk', 'date_begin', 'date_end', 'status')
    list_filter = ('status',)


@admin.register(RemediationPlanAnswer)
class RemediationPlanAnswerAdmin(admin.ModelAdmin):
    model = RemediationPlanAnswer
    list_display = ('remediation_plan', 'user', 'created')
