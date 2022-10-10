"""Booking model."""
import os
import hashlib
import random

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel


class CompanyDomainRiskEvaluator(AuditModel):

    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE
    )

    domain_risk = models.ForeignKey(
        'risks.Domainrisk',
        on_delete=models.CASCADE
    )

    evaluator = models.ManyToManyField(
        'users.User',
        verbose_name=_('Evaluadores'),
        blank=True
    )

    def __str__(self):
        return f'{self.company} - {self.domain_risk}'

    class Meta:
        verbose_name = _("Evaluador de Dominio de Riesgo para Compañía")
        verbose_name_plural = _(
            "Evaluadores de Dominios de Riesgo para Compañías")
        ordering = ["company", "domain_risk"]
