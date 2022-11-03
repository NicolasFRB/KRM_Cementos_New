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
from krm.risks.models import risk_company_model
from django.db.models import Avg

# Utilities
from krm.utils.models import AuditModel


class RiskCompanyResidual(AuditModel):

    evaluation = models.ForeignKey(
        "evaluations_krm.EvaluationKrmResidual",
        verbose_name=_("Evaluación de riesgo residual"),
        related_name="risk_company_residuals",
        on_delete=models.CASCADE,
    )

    risk_company = models.ForeignKey(
        "risks.RiskCompany",
        related_name="risk_company_residuals",
        on_delete=models.CASCADE
    )

    RISK_CHOICES = (
        (0, _('Sin establecer')),
        (1, _('Optimizado')),
        (2, _('Aceptable')),
        (3, _('Inadecuado')),
        (4, _('No controlado')),
        (5, _('N/A')),
    )

    probability_level_residual_administrator = models.PositiveSmallIntegerField(
        _('Nivel de Control asignado por el Administrador de la compañía'),
        choices=RISK_CHOICES,
        default=0
    )

    description_administrator = models.TextField(
        verbose_name=_(
            "Descripción de la evaluación por el Administrador de la compañía"),
        help_text=_(
            "En caso de estar pegando desde el portapapeles asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 8000 caracteres considere incluirlo como una evidencia"
        ),
        max_length=10000,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.evaluation.ref} - {self.risk_company.risk.name}'

    class Meta:
        verbose_name = _("Evaluación de Riesgo Compañía Residual Agregado")
        verbose_name_plural = _(
            "Evaluaciones de Riesgo Compañía Residual Agregados")

    @property
    def get_latest_impact_inherent(self):
        # Evaluaciones en las que se ha evaluado ese riesgo compañía
        if self.risk_company.risk_test_inherent.filter(
            status=3,
            evaluation__status='FI'
        ).count() > 0:
            last_evaluate_risk_inherent = self.risk_company.risk_test_inherent.filter(
                status=3,
                evaluation__status='FI'
            ).order_by('evaluation__date_begin').first()
            return last_evaluate_risk_inherent.impact_level_administrator

        return None

    @property
    def get_latest_probability_inherent(self):
        # Evaluaciones en las que se ha evaluado ese riesgo compañía
        if self.risk_company.risk_test_inherent.filter(
            status=3,
            evaluation__status='FI'
        ).count() > 0:
            last_evaluate_risk_inherent = self.risk_company.risk_test_inherent.filter(
                status=3,
                evaluation__status='FI'
            ).order_by('evaluation__date_begin').first()
            return last_evaluate_risk_inherent.probability_level_administrator

        return None

    @property
    def probability_level_residual_evaluator_aggregate(self):
        """
          Función que devuelve la media de valores de probabilidad residual de todos los valores dados por los usuarios evaluadores
        """
        from krm.evaluations_krm.models import RiskTestResidual

        probability_level_residual_evaluator_avg = RiskTestResidual.objects.filter(
            evaluation=self.evaluation,
            risk=self.risk_company,
            status=2
        ).exclude(
            probability_level_residual_evaluator=5
        ).aggregate(Avg('probability_level_residual_evaluator'))

        if probability_level_residual_evaluator_avg['probability_level_residual_evaluator__avg'] is None:
            return 0.0

        return probability_level_residual_evaluator_avg['probability_level_residual_evaluator__avg']

    @property
    def probability_level_residual_evaluator_aggregate_rounded(self):
        return round(self.probability_level_residual_evaluator_aggregate)

    @property
    def risk_test_residuals(self):
        """
          Función que devuelve todas las descripciones dadas por los evaluadores
        """
        from krm.evaluations_krm.models import RiskTestResidual

        return RiskTestResidual.objects.filter(
            evaluation=self.evaluation,
            risk=self.risk_company,
            status=2
        )

    def get_controls_attempt_to_mitigate(self):
        """
          Función que devuelve todos los controles que intentan mitigar al riesgo que se está evaluando y que afectan a la compañía en cuestión
        """
        from krm.controls.models import Control
        # Controles que aplican a esa compañía, los cuales están asociados al riesgo de este test de riesgo residual
        controls = Control.objects.filter(
            risks__id__exacts=self.risk_company.risk.pk,
            pk__in=[control.pk for control in self.evaluation.company.controls.all()]
        )
        return controls

    def get_test_controls_attempt_to_mitigate(self):
        """
          Función que devuelve todos los test de riesgo evaluados para los controles que intentan mitigar al riesgo que se está evaluando y que afecta a la compañía
        """

        from krm.evaluations.models import ControlTest

        # Miramos si hay test de control lanzados para los controles asociados a ese riesgo compañía
        control_tests = ControlTest.objects.filter(
            evaluation__company=self.evaluation.company,
            control__pk__in=[
                c.pk for c in self.get_controls_attempt_to_mitigate],
            status='FI'
        )

        return control_tests
