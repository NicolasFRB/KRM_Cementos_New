"""Booking model."""
import os
import hashlib
import random

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel


class CompanyQuestionnaireEvaluator(AuditModel):

    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='domain_risk_evaluators'
    )

    evaluator = models.ManyToManyField(
        'users.User',
        verbose_name=_('Cumplimentador de Cuestionarios'),
        blank=True
    )

    def __str__(self):
        return f'{self.company} - {self.evaluator}'

    class Meta:
        verbose_name = _("Evaluador de Cuestionario para Compañía")
        verbose_name_plural = _(
            "Evaluadores de Cuestionarios para Compañías")
        ordering = ["company", "evaluator"]
