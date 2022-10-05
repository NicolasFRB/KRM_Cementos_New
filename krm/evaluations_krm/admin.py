from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from krm.evaluations_krm.models import (
    EvaluationKrmInherent,
    RiskTestInherent
)


@admin.register(EvaluationKrmInherent)
class EvaluationKrmInherentAdmin(admin.ModelAdmin):
    model = EvaluationKrmInherent
    list_display = ('ref', 'company', 'status', 'date_begin')
    list_filter = ('status', 'company')


@admin.register(RiskTestInherent)
class RiskTestInherentAdmin(admin.ModelAdmin):
    model = RiskTestInherent
    list_display = (
        'evaluation',
        'risk',
        'expert',
        'impact_level_expert',
        'probability_level_expert',
        'impact_level_administrator',
        'probability_level_administrator'
    )
    list_filter = ('evaluation__company', 'evaluation')
