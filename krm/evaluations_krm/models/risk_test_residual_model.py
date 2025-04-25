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

from krm.configuration.models import Configuration
from krm.evaluations_krm.models import RiskTestInherent


class RiskTestResidual(AuditModel):

    evaluation = models.ForeignKey(
        "evaluations_krm.EvaluationKrmResidual",
        verbose_name=_("Evaluación de riesgo residual"),
        related_name="risk_test_residuals",
        on_delete=models.CASCADE,
    )

    risk = models.ForeignKey(
        "risks.RiskCompany",
        related_name="risk_test_residual",
        on_delete=models.CASCADE
    )

    evaluator = models.ForeignKey(
        "users.User",
        verbose_name=_("Evaluador"),
        related_name="risk_test_residuals",
        on_delete=models.CASCADE,
    )

    IMPACT_CHOICES = (
        (0, _('Sin establecer')),
        (1, _('Muy bajo')),
        (2, _('Bajo')),
        (3, _('Medio')),
        (4, _('Alto')),
        (5, _('Muy alto')),
    )

    PROBABILITY_CHOICES= (
        (0, _('Sin establecer')),
        (1, _("Remoto")),
        (2, _("Posible")),
        (3, _("Probable")),
        (4, _("Muy probable")),
        (5, _("Prácticamente cierto")),
    )

    EVENT_SPEED_CHOICES= (
        (0, _('Sin establecer')),
        (1, _('Muy baja')),
        (2, _('Baja')),
        (3, _('Media')),
        (4, _('Alta')),
        (5, _('Muy alta')),
    )

    impact_reputational_evaluator= models.PositiveSmallIntegerField(
        _('Nivel de Impacto Reputacional indicado por el Evaluador'),
        choices=IMPACT_CHOICES,
        default=0
    )

    impact_economic_evaluator = models.PositiveSmallIntegerField(
        _('Nivel de Impacto Económico indicado por el Evaluador'),
        choices=IMPACT_CHOICES,
        default=0
    )

    impact_regulatory_evaluator = models.PositiveSmallIntegerField(
        _('Nivel de Impacto Regulatorio indicado por el Evaluador'),
        choices=IMPACT_CHOICES,
        default=0
    )

    impact_objectives_evaluator = models.PositiveSmallIntegerField(
        _('Nivel de Impacto en los objetivos estratégicos por el Evaluador'),
        choices=IMPACT_CHOICES,
        default=0
    )

    impact_dedication_evaluator = models.PositiveSmallIntegerField(
        _('Nivel de Impacto en el tiempo de dedicación del Comité de Dirección indicado por el Evaluador'),
        choices=IMPACT_CHOICES,
        default=0
    )

    impact_level_evaluator = models.PositiveSmallIntegerField(
        _('Nivel de Impacto indicado por el Evaluador'),
        choices= IMPACT_CHOICES,
        default=0
    )

    probability_level_evaluator = models.PositiveSmallIntegerField(
        _('Nivel de Probabilidad residual indicado por el Evaluador'),
        choices=PROBABILITY_CHOICES,
        default=0
    )

    event_speed_level_evaluator = models.PositiveSmallIntegerField(
        _('Nivel de Velocidad de ocurrencia indicado por el Evaluador'),
        choices=EVENT_SPEED_CHOICES,
        default=0
    )

    description_evaluator = models.TextField(
        verbose_name=_(
            "Descripción de la valoración del Evaluador"),
        help_text=_(
            "En caso de estar pegando desde el portapapeles asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 8000 caracteres considere incluirlo como una evidencia"
        ),
        max_length=10000,
        null=True,
        blank=True,
    )

    impact_level_administrator= models.PositiveSmallIntegerField(
        _('Nivel de Impacto indicado por el Administrador'),
        choices=IMPACT_CHOICES,
        default=0
    )

    probability_level_administrator= models.PositiveSmallIntegerField(
        _('Nivel de Probabilidad indicado por el Administrador'),
        choices=PROBABILITY_CHOICES,
        default=0
    )

    event_speed_level_administrator = models.PositiveSmallIntegerField(
        _('Nivel de Velocidad de ocurrencia indicado por el Administrador'),
        choices=EVENT_SPEED_CHOICES,
        default=0
    )

    description_administrator = models.TextField(
        verbose_name=_(
            "Descripción de la valoración del Administrador de compañía"),
        help_text=_(
            "En caso de estar pegando desde el portapapeles asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 8000 caracteres considere incluirlo como una evidencia"
        ),
        max_length=10000,
        null=True,
        blank=True,
    )

    STATUS_CHOICES = (
        (0, _('Sin iniciar')),
        (1, _('En espera del Evaluador')),
        (2, _('En espera del Administrador')),
        (3, _('Finalizado')),
    )

    status = models.PositiveSmallIntegerField(
        _('Estado'),
        choices=STATUS_CHOICES,
        default=0
    )

    severity_level_evaluator=  models.IntegerField(
        _('Nivel de severidad indicado por el Evaluador'),
        default=0
    )

    severity_level_administrator = models.IntegerField(
        _('Nivel de severidad del administrador'),
        default=0
    )

    SEVERITY_CHOICES= (
        ("SE", _('Sin establecer')),
        ("MB", _('Muy baja')),
        ("B", _('Baja')),
        ("M", _('Media')),
        ("A", _('Alta')),
        ("MA", _('Muy alta'))
    )

    severity_evaluator_qualitative= models.CharField(
        _("Severidad cualitativa indicada por el Evaluador"),
        max_length=2,
        choices= SEVERITY_CHOICES,
        default="SE",
    )

    severity_administrator_qualitative= models.CharField(
        _("Severidad cualitativa indicada por el Administrador"),
        max_length=2,
        choices= SEVERITY_CHOICES,
        default="SE",
    )

    def qualitative_severity(self, language, role):
        """
        Método de la clase de test de riesgo residual que nos proporciona el valor cualitativo en la lengua introducida (español/inglés)
        de la severidad proporcionada por el usuario con rol introducido (evaluador/supervisor).

        Es por ello, que los valores "soportados" por esta función son los siguientes:
            language: Cadena de texto "es" (español), "en" (inglés), "bd" (base de datos). Introducimos esta última opción para guardar los valores
            correspondientes cuando se aporta valoración por parte del evaluador/administrador y se ha de calcular el valor cualitativo para guardarlo en las variables.
            role: Cadena de texto "evaluator" (evaluador del riesgo), "administrator" (administrador de compañía).
        En caso de que los valores introducidos como parámetros de entrada no se correspondan con ninguno de los anteriores, se devolverá None.
        """
        if role== 'evaluator':
            severity = self.severity_level_evaluator
        elif role== 'administrator':
            severity= self.severity_level_administrator
        else:
            return None
        if severity == 0:
            value= ["Sin establecer", "Not stablished", "SE"]
        elif 1 <= severity <= 4:
            if self.severity_level_evaluator==4 and (self.impact_level_evaluator==1 or self.probability_level_evaluator==1):
                value= ["Baja", "Low", "B"]
            else:
                value= ["Muy baja", "Very low", "MB"]
        elif severity == 5:
            value= ["Media", "Medium", "M"]
        elif severity == 6:
            value= ["Baja", "Low", "B"]
        elif 7<= severity <=12:
            value= ["Media", "Medium", "M"]
        elif 13 <= severity <= 20:
            value= ["Alta", "High", "A"]
        elif 21 <= severity <= 25:
            value= ["Muy alta", "Very high", "MA"]
        if language== "es":
            return value[0]
        elif language== "en":
            return value[1]
        elif language=="bd":
            return value[2]
        else:
            return None

    def __str__(self):
        return f'{self.evaluation.ref} - {self.risk.risk.name}'

    def translation_values(self, value):
        if value==0:
            return "Not established"
        elif value==1:
            return "Very low"
        elif value==2:
            return "Low"
        elif value== 3:
            return "Medium"
        elif value==4:
            return "High"
        elif value==5:
            return "Very high"

    # @property
    # def probability_level_residual_evaluator_qualitative(self):
    #     p = self.probability_level_residual_evaluator
    #     if p <= 1: return "Optimizado"
    #     if p <= 2: return "Aceptable"
    #     if p <= 3: return "Inadecuado"
    #     if p <= 4: return "No controlado"
    #     if p <= 5: return "N/A"
    #     return "Sin establecer"

    @property
    def get_inherent_risk_tests(self):
        """
        Método de la clase test de riesgo residual el cual nos devuelve
        """

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk=self.risk,
            evaluation__status='FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent

        return None

    @property
    def get_latest_impact_inherent(self):

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk=self.risk,
            evaluation__status='FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().impact_level_administrator

        return None

    @property
    def get_latest_probability_inherent(self):

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk=self.risk,
            evaluation__status='FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().probability_level_administrator

        return None

    @property
    def get_latest_event_speed_inherent(self):

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk=self.risk,
            evaluation__status='FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().event_speed_level_administrator

        return None

    @property
    def get_latest_justification_inherent(self):

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk=self.risk,
            evaluation__status='FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().description_administrator

        return None

    @property
    def get_latest_severity_inherent(self):

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk=self.risk,
            evaluation__status='FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().severity_level_administrator

        return None

    @property
    def get_latest_severity_inherent_qualitative(self):

        last_evaluate_risk_inherent = RiskTestInherent.objects.filter(
            risk=self.risk,
            evaluation__status='FI',
        )

        if last_evaluate_risk_inherent.count() > 0:
            return last_evaluate_risk_inherent.order_by('evaluation__date_begin').first().get_severity_administrator_qualitative_display

        return None

    @property
    def controls_attempt_to_mitigate(self):
        return self.get_controls_attempt_to_mitigate()

    def get_controls_attempt_to_mitigate(self):
        """
        Método de la clase que recupera los controles asociados al Riesgo N2 que queremos
        testear en este test de riesgo.
        """
        from krm.controls.models import Control
        from krm.companies.models import CompanyControls
        controls = Control.objects.filter(
            risks__id__exact=self.risk.risk.pk,
            pk__in=[control.control.pk for control in CompanyControls.objects.filter(company=self.evaluation.company, active=True)]
        )
        return controls

    class Meta:
        verbose_name = _("Test de Riesgo Residual")
        verbose_name_plural = _("Tests de Riesgo Residual")

    def save(self, *args, **kwargs):
        """
        Método de almacenamiento del test de riesgo residual, el cual controla la actualización de los parámetros
        que dependen de una transformación tras la aportación de datos del usuario.

        Este almacenamiento se ejecuta con el método save de un AuditModel, el cual guarda los valores para los atributos en la base de datos.
        Anteriormente la condición del almacenamiento de estos datos dependía del estado del test de riesgo, actualmente este método
        es llamado a través de ciertas vistas que controlan la valoración de un test de riesgo. De manera que cuando se aporta una valoración
        se almacenan los atributos dependientes con este método.
        """
        self.impact_level_evaluator = max(self.impact_reputational_evaluator,
                                       self.impact_economic_evaluator,
                                       self.impact_regulatory_evaluator,
                                       self.impact_objectives_evaluator,
                                       self.impact_dedication_evaluator
                                    )

        self.severity_level_evaluator = self.impact_level_evaluator * self.probability_level_evaluator
        self.severity_level_administrator = self.impact_level_administrator * self.probability_level_administrator
        self.severity_evaluator_qualitative= self.qualitative_severity("bd", "evaluator")
        self.severity_administrator_qualitative= self.qualitative_severity("bd", "administrator")

        super().save(*args, **kwargs)

    def send_notification_evaluator(self, notif_type):
        from krm.evaluations_krm.tasks import (
            risk_test_send_notification_evaluator,
        )
        # risk_test_send_notification_evaluator.delay(self.pk, notif_type)
        risk_test_send_notification_evaluator(self.pk, notif_type)

    def send_email_notification_evaluator(self, notif_type):
        from krm.configuration.models import Configuration

        configuration = Configuration.objects.first()

        translation.activate(self.evaluator.notification_language)

        # Esto notificará al control owner de que tiene controles por rellenar
        if self.evaluation.certification_period:
            period = " (%s)" % self.evaluation.certification_period
        else:
            period = ""
        context = {
            "site_url": settings.SITE_URL,
            "recovery_url": settings.SITE_URL + reverse("auth:remember_password_form"),
            "user_email": self.evaluator.email,
            "evaluation_ref": self.evaluation.ref,
            "evaluation_date_begin": self.evaluation.date_begin,
            "evaluation_date_end": self.evaluation.date_end,
            "certification_year": self.evaluation.certification_year,
            "certification_period": period,
            "app_name": configuration.app_name,
            "notif_type": notif_type,
        }
        body_html = render_to_string(
            "emails/risk_test_residual/risk_test_email_evaluator.html", context
        )
        context = {
            "content": body_html,
            "preheader": _("Test de Riesgos pendientes de valorar"),
            "BRAND": settings.BRAND,
            "app_name": configuration.app_name,
        }
        body_html = render_to_string("emails/base-inline.html", context)
        from_email = settings.EMAIL_FROM
        if settings.EMAIL_BCC:
            bcc = settings.EMAIL_BCC
        else:
            bcc = ""

        subject, from_email, to = (
            _("{} - Test de Riesgos pendientes de valorar".format(configuration.app_name)),
            from_email,
            self.evaluator.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.evaluator.add_action(
            _("[%s] Envío de email de Test de Riesgos Residuales pendientes de valorar (%s)" % (notif_type.upper(), self.evaluation.ref)))

        if configuration.enable_emails:
            return msg.send(fail_silently=False)

