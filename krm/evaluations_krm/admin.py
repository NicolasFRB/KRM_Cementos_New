from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from krm.evaluations_krm.models import (
    EvaluationKrmInherent,
    RiskTestInherent,
    EvaluationKrmResidual,
    RiskTestResidual
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


@admin.register(EvaluationKrmResidual)
class EvaluationKrmResidualAdmin(admin.ModelAdmin):
    model = EvaluationKrmResidual
    list_display = ('ref', 'company', 'status', 'date_begin')
    list_filter = ('status', 'company')


@admin.register(RiskTestResidual)
class RiskTestResidualAdmin(admin.ModelAdmin):
    model = RiskTestResidual
    list_display = (
        'evaluation',
        'risk',
    )
    list_filter = ('evaluation__company', 'evaluation')
