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

    RISK_CHOICES = (
        (1, _('Bajo')),
        (2, _('Medio')),
        (3, _('Alto')),
        (4, _('Crítico')),
        (5, _('Sin establecer')),
    )

    probability_level_residual_evaluator = models.PositiveSmallIntegerField(
        _('Nivel de Probabilidad residual indicado por el Evaluador del Dominio de Riesgo'),
        choices=RISK_CHOICES,
        default=5
    )

    description_evaluator = models.TextField(
        verbose_name=_(
            "Descripción de la evaluación por el Evaluador del Dominio de Riesgo asociado"),
        help_text=_(
            "En caso de estar pegando desde el portapapeles asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 8000 caracteres considere incluirlo como una evidencia"
        ),
        max_length=10000,
        null=True,
        blank=True,
    )

    probability_level_residual_administrator = models.PositiveSmallIntegerField(
        _('Nivel de Probabilidad residual indicado por el Admnistrador de la compañía'),
        choices=RISK_CHOICES,
        default=5
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

    STATUS_CHOICES = (
        (0, _('Sin iniciar')),
        (1, _('Esperando al Evaluador de Dominio de Riesgo')),
        (2, _('Esperando al Administrador')),
        (3, _('Finalizado')),
    )

    status = models.PositiveSmallIntegerField(
        _('Estado'),
        choices=STATUS_CHOICES,
        default=0
    )

    def __str__(self):
        return f'{self.evaluation.ref} - {self.risk.risk.name}'

    class Meta:
        verbose_name = _("Test de Riesgo Residual")
        verbose_name_plural = _("Tests de Riesgo Residual")

    def send_notification_evaluator(self):
        from krm.evaluations_krm.tasks import (
            risk_test_send_notification_evaluator,
        )
        risk_test_send_notification_evaluator.delay(self.pk)

    def send_email_notification_evaluator(self):
        # Esto notificará al control owner de que tiene controles por rellenar
        context = {
            "site_url": settings.SITE_URL,
            "recovery_url": settings.SITE_URL + reverse("auth:remember_password_form"),
            "user_email": self.evaluator.email,
            "evaluation_ref": self.evaluation.ref,
            "evaluation_date_begin": self.evaluation.date_begin,
            "evaluation_date_end": self.evaluation.date_end,
        }
        body_html = render_to_string(
            "emails/risk_test_residual/risk_test_email_evaluator.html", context
        )
        context = {
            "content": body_html,
            "preheader": _("Test de Riesgos pendientes de valorar"),
        }
        body_html = render_to_string("emails/base-inline.html", context)
        from_email = settings.EMAIL_FROM
        if settings.EMAIL_BCC:
            bcc = settings.EMAIL_BCC
        else:
            bcc = ""

        subject, from_email, to = (
            _("KRM Tool - Test de Riesgos pendientes de valorar"),
            from_email,
            self.evaluator.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.evaluator.add_action(
            _("Envío de email de Test de Riesgos pendientes de valorar"))
        msg.send(fail_silently=False)
