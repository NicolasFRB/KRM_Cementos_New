"""ControlTest model."""

import random

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Utilities
from krm.utils.models import AuditModel


class RiskTestInherent(AuditModel):

    evaluation = models.ForeignKey(
        "evaluations_krm.EvaluationKrmInherent",
        verbose_name=_("Evaluación de riesgo inherente"),
        related_name="evaluation",
        on_delete=models.CASCADE,
    )

    risk = models.ForeignKey(
        "risks.RiskCompany",
        related_name="risk_test",
        on_delete=models.CASCADE
    )

    expert = models.ForeignKey(
        "users.User",
        verbose_name=_("Experto"),
        related_name="risk_test_inherents",
        on_delete=models.CASCADE,
    )

    RISK_CHOICES = (
        (0, _('No aplica')),
        (1, _('Bajo')),
        (2, _('Medio')),
        (3, _('Alto')),
        (4, _('Crítico')),
        (5, _('Sin establecer')),
    )

    impact_level_expert = models.PositiveSmallIntegerField(
        _('Impacto'),
        choices=RISK_CHOICES,
        default=5
    )

    probability_level_expert = models.PositiveSmallIntegerField(
        _('Probabilidad'),
        choices=RISK_CHOICES,
        default=5
    )

    impact_level_administrator = models.PositiveSmallIntegerField(
        _('Impacto'),
        choices=RISK_CHOICES,
        default=5
    )

    probabilityimpact_level_administrator = models.PositiveSmallIntegerField(
        _('Probabilidad'),
        choices=RISK_CHOICES,
        default=5
    )

    def __str__(self):
        return f'{self.evaluation.ref} - {self.risk.risk.name}'

    class Meta:
        verbose_name = _("Test de Riesgo Inherente")
        verbose_name_plural = _("Tests de Riesgo Inherente")
