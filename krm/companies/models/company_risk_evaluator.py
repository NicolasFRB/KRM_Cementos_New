# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel


class CompanyRiskEvaluator(AuditModel):

    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='risk_evaluators'
    )

    risk = models.ForeignKey(
        'risks.Risk',
        on_delete=models.CASCADE
    )

    evaluator = models.ManyToManyField(
        'users.User',
        verbose_name=_('Evaluadores'),
        blank=True
    )

    def __str__(self):
        return f'{self.company.name} - {self.risk.ref}'

    class Meta:
        verbose_name = _("Evaluador de Riesgo para Compañía")
        verbose_name_plural = _(
            "Evaluadores de Riesgo para Compañías")
        ordering = ["company", "risk"]
