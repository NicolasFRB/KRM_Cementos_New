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
        verbose_name = _("Evaluación de Riesgo Residual Agregada")
        verbose_name_plural = _(
            "Evaluaciones de Riesgo Residual Agregadas")

    @property
    def probability_residual_administrator_qualitative(self):
        p = self.probability_level_residual_administrator
        if p == 0: return "Sin establecer"
        if p <= 1: return "Optimizado"
        if p <= 2: return "Aceptable"
        if p <= 3: return "Inadecuado"
        if p <= 4: return "No controlado"
        return "Sin establecer"

    @property
    def get_latest_inherent(self):
        # Evaluaciones en las que se ha evaluado ese riesgo compañía
        from krm.evaluations_krm.models import RiskTestInherent

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk = self.risk_company,
            evaluation__status = 'FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first()

        return None
    
    @property
    def get_latest_impact_inherent(self):
        # Evaluaciones en las que se ha evaluado ese riesgo compañía
        from krm.evaluations_krm.models import RiskTestInherent

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk = self.risk_company,
            evaluation__status = 'FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().impact_level_administrator

        return None

    @property
    def get_latest_probability_inherent(self):
        # Evaluaciones en las que se ha evaluado ese riesgo compañía
        from krm.evaluations_krm.models import RiskTestInherent

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk = self.risk_company,
            evaluation__status = 'FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().probability_level_administrator

        return None

    @property
    def get_latest_justification_inherent(self):
        # Evaluaciones en las que se ha evaluado ese riesgo compañía
        from krm.evaluations_krm.models import RiskTestInherent

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk = self.risk_company,
            evaluation__status = 'FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().description_admin

        return None

    @property
    def get_latest_severity_inherent(self):
        # Evaluaciones en las que se ha evaluado ese riesgo compañía
        from krm.evaluations_krm.models import RiskTestInherent

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk = self.risk_company,
            evaluation__status = 'FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().severity_level_admin

        return None

    @property
    def get_latest_severity_inherent_qualitative(self):
        # Evaluaciones en las que se ha evaluado ese riesgo compañía
        from krm.evaluations_krm.models import RiskTestInherent

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk = self.risk_company,
            evaluation__status = 'FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().severity_level_admin_qualitative

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
            status__in=[2,3],
            probability_level_residual_evaluator__in = [1,2,3,4],
        ).exclude(
            probability_level_residual_evaluator=5
        ).aggregate(Avg('probability_level_residual_evaluator'))

        if probability_level_residual_evaluator_avg['probability_level_residual_evaluator__avg'] is None:
            return 0.0

        # Round to 2 decimals
        return round(probability_level_residual_evaluator_avg['probability_level_residual_evaluator__avg'], 2)

    @property
    def probability_level_residual_evaluator_aggregate_rounded(self):
        return round(self.probability_level_residual_evaluator_aggregate)

    @property
    def probability_residual_evaluator_qualitative(self):
        p = self.probability_level_residual_evaluator_aggregate_rounded
        if p <= 1: return "No significativo"
        if p <= 2: return "Bajo"
        if p <= 3: return "Alto"
        if p <= 4: return "Crítico"
        return "Sin establecer"

    @property
    def probability_level_result_evaluator(self):
        p = self.probability_level_residual_evaluator_aggregate_rounded
        p_i = self.get_latest_probability_inherent

        # Si no hay evaluaciones residuales (p==0)
        # o no hay nivel de control (p==4)
        # o todo está sin tocar (p==5)
        # return inherente == residual
        if p == 0 or p == 4 or p == 5:
            return p_i

        # Reglas de negocio
        if p == 1: 
            r = p_i - 3
        elif p == 2:
            r = p_i - 2
        elif p == 3:
            r = p_i - 1
        
        # Si residual fuera de escala (1,4): min escala (1) 
        if r < 1:
            r = 1

        return r

    @property
    def probability_level_result_admin(self):
        p = self.probability_level_residual_administrator
        p_i = self.get_latest_probability_inherent

        # Si no hay evaluaciones residuales (p==0)
        # o no hay nivel de control (p==4)
        # o todo está sin tocar (p==5)
        # return inherente == residual
        if p == 0 or p == 4 or p == 5:
            return p_i

        # Reglas de negocio
        if p == 1: 
            r = p_i - 3
        elif p == 2:
            r = p_i - 2
        elif p == 3:
            r = p_i - 1
        
        # Si residual fuera de escala (1,4): min escala (1) 
        if r < 1:
            r = 1

        return r

    @property
    def severity_residual_evaluator(self):
        return self.probability_level_result_evaluator * self.get_latest_impact_inherent

    @property
    def severity_residual_evaluator_qualitative(self):
        sev = self.severity_residual_evaluator
        if sev == 0: return 0
        if sev <= 2: return "No significativo"
        if sev <= 5: return "Bajo"
        if sev <= 11: return "Alto"
        if sev <= 16: return "Crítico"

    @property
    def severity_residual_admin(self):
        return self.probability_level_result_admin * self.get_latest_impact_inherent

    @property
    def severity_residual_admin_qualitative(self):
        sev = self.severity_residual_admin
        if sev == 0: return 0
        if sev <= 2: return "No significativo"
        if sev <= 5: return "Bajo"
        if sev <= 11: return "Alto"
        if sev <= 16: return "Crítico"

    @property
    def risk_test_residuals(self):
        """
          Función que devuelve todas las descripciones dadas por los evaluadores
        """
        from krm.evaluations_krm.models import RiskTestResidual

        return RiskTestResidual.objects.filter(
            evaluation=self.evaluation,
            risk=self.risk_company,
            status__in = [2, 3],
        )

    @property
    def risk_test_residuals_calculus(self):
        """
          Función que devuelve todas las descripciones dadas por los evaluadores
        """
        from krm.evaluations_krm.models import RiskTestResidual

        return RiskTestResidual.objects.filter(
            evaluation=self.evaluation,
            risk=self.risk_company,
            status__in = [2, 3],
            probability_level_residual_evaluator__in = [1,2,3,4],
        )

    @property
    def risk_test_residuals_all(self):
        """
          Función que devuelve todas las descripciones dadas por los evaluadores
        """
        from krm.evaluations_krm.models import RiskTestResidual

        return RiskTestResidual.objects.filter(
            evaluation=self.evaluation,
            risk=self.risk_company,
        )

    def get_controls_attempt_to_mitigate(self):
        from krm.controls.models import Control
        from krm.companies.models import CompanyControls
        # Controles que aplican a esa compañía, los cuales están asociados al riesgo de este test de riesgo residual
        print(CompanyControls.objects.filter(company=self.evaluation.company))
        controls = Control.objects.filter(
            risks__id__exact=self.risk_company.risk.pk)
        return controls

    def get_test_controls_attempt_to_mitigate(self):
        from krm.evaluations.models import ControlTest

        # Miramos si hay test de control lanzados para los controles asociados a ese riesgo compañía
        control_tests = ControlTest.objects.filter(
            evaluation__company=self.evaluation.company,
            control__pk__in=[
                c.pk for c in self.get_controls_attempt_to_mitigate()],
            status='FI'
        )

        return control_tests
