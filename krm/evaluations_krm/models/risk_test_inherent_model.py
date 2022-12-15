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


class RiskTestInherent(AuditModel):

    evaluation = models.ForeignKey(
        "evaluations_krm.EvaluationKrmInherent",
        verbose_name=_("Evaluación de riesgo inherente"),
        related_name="risk_test_inherents",
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
        (1, _('No significativo')),
        (2, _('Bajo')),
        (3, _('Alto')),
        (4, _('Crítico')),
        (5, _('Sin establecer')),
    )

    impact_economic_level_expert = models.PositiveSmallIntegerField(
        _('Nivel de Impacto Económico indicado por el Experto del Dominio de Riesgo'),
        choices=RISK_CHOICES,
        default=5
    )

    impact_continuity_level_expert = models.PositiveSmallIntegerField(
        _('Nivel de Impacto en Continuidad indicado por el Experto del Dominio de Riesgo'),
        choices=RISK_CHOICES,
        default=5
    )

    impact_branding_level_expert = models.PositiveSmallIntegerField(
        _('Nivel de Impacto en Imagen indicado por el Experto del Dominio de Riesgo'),
        choices=RISK_CHOICES,
        default=5
    )

    impact_level_expert = models.PositiveSmallIntegerField(
        _('Nivel de Impacto indicado por el Experto del Dominio de Riesgo'),
        choices=RISK_CHOICES,
        default=5
    )

    probability_level_expert = models.PositiveSmallIntegerField(
        _('Nivel de Probabilidad indicado por el Experto del Dominio de Riesgo'),
        choices=RISK_CHOICES,
        default=5
    )

    impact_level_administrator = models.PositiveSmallIntegerField(
        _('Nivel de Impacto indicado por el Administrador del Dominio de Riesgo'),
        choices=RISK_CHOICES,
        default=5
    )

    probability_level_administrator = models.PositiveSmallIntegerField(
        _('Nivel de Probabilidad indicado por el Administrador del Dominio de Riesgo'),
        choices=RISK_CHOICES,
        default=5
    )

    STATUS_CHOICES = (
        (0, _('Sin iniciar')),
        (1, _('Esperando al Experto de Dominio de Riesgo')),
        (2, _('Esperando al Administrador')),
        (3, _('Finalizado')),
    )

    status = models.PositiveSmallIntegerField(
        _('Estado'),
        choices=STATUS_CHOICES,
        default=0
    )

    description = models.TextField(
        verbose_name=_(
            "Descripción de la evaluación por el Experto del Dominio de Riesgo asociado"),
        help_text=_(
            "En caso de estar pegando desde el portapapeles asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 8000 caracteres considere incluirlo como una evidencia"
        ),
        max_length=10000,
        null=True,
        blank=True,
    )

    description_admin = models.TextField(
        verbose_name=_(
            "Descripción de la evaluación por el Administrador de la Compañía Evaluada"),
        help_text=_(
            "En caso de estar pegando desde el portapapeles asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 8000 caracteres considere incluirlo como una evidencia"
        ),
        max_length=10000,
        null=True,
        blank=True,
    )

    severity_level_expert = models.IntegerField(
        _('Nivel de severidad del experto'),
        default=0
    )

    severity_level_admin = models.IntegerField(
        _('Nivel de severidad del administrador'),
        default=0
    )

    @property
    def severity_level_expert_qualitative(self):
        sev = self.severity_level_expert
        if sev == 0:
            return 0
        if sev <= 2:
            return "No significativo"
        if sev <= 5:
            return "Bajo"
        if sev <= 11:
            return "Alto"
        if sev <= 16:
            return "Crítico"

    @property
    def severity_level_admin_qualitative(self):
        sev = self.severity_level_admin
        if sev == 0:
            return 0
        if sev <= 2:
            return "No significativo"
        if sev <= 5:
            return "Bajo"
        if sev <= 11:
            return "Alto"
        if sev <= 16:
            return "Crítico"

    def __str__(self):
        return f'{self.evaluation.ref} - {self.risk.risk.name}'

    class Meta:
        verbose_name = _("Test de Riesgo Inherente")
        verbose_name_plural = _("Tests de Riesgo Inherente")

    def save(self, *args, **kwargs):
        self.impact_level_expert = max(self.impact_branding_level_expert,
                                       self.impact_continuity_level_expert,
                                       self.impact_economic_level_expert
                                       )
        # Severity level expert
        if self.status >= 2:
            self.severity_level_expert = self.impact_level_expert * self.probability_level_expert

        if self.status >= 2:
            self.severity_level_admin = self.impact_level_administrator * \
                self.probability_level_administrator

        super().save(*args, **kwargs)

    def send_notification_expert(self):
        from krm.evaluations_krm.tasks import (
            risk_test_send_notification_expert,
        )
        risk_test_send_notification_expert.delay(self.pk)

    def sent_email_notification_expert(self):
        from krm.configuration.models import Configuration

        configuration = Configuration.objects.first()

        context = {
            "site_url": settings.SITE_URL,
            "recovery_url": settings.SITE_URL + reverse("auth:remember_password_form"),
            "user_email": self.expert.email,
            "evaluation_ref": self.evaluation.ref,
            "evaluation_date_begin": self.evaluation.date_begin,
            "evaluation_date_end": self.evaluation.date_end,
        }
        body_html = render_to_string(
            "emails/risk_test_inherent/risk_test_email_expert.html", context
        )
        context = {
            "content": body_html,
            "preheader": _("Test de Riesgos pendientes de valorar"),
            "BRAND": settings.BRAND
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
            self.expert.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.expert.add_action(
            _("Envío de email de Test de Riesgos pendientes de valorar"))

        if configuration.enable_emails:
            msg.send(fail_silently=False)
