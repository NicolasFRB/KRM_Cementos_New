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


class QuestionTest(AuditModel):

    evaluation = models.ForeignKey(
        "questionnaires.EvaluationQuestionnaire",
        verbose_name=_("Evaluación de cuestionario"),
        related_name="question_tests",
        on_delete=models.CASCADE,
    )

    question = models.ForeignKey(
        "questionnaires.Question",
        related_name="question_tests",
        on_delete=models.SET_NULL,
        null=True
    )

    evaluator = models.ForeignKey(
        "users.User",
        verbose_name=_("Evaluador"),
        related_name="question_tests",
        on_delete=models.CASCADE,
    )

    RESULT_CHOICES = (
        (0, _('Sin establecer')),
        (1, _('Si')),
        (2, _('No')),
        (3, _('No aplica')),
    )

    answer = models.PositiveSmallIntegerField(
        _('Respuesta'),
        choices=RESULT_CHOICES,
        default=0
    )

    STATUS_CHOICES = (
        (0, _('Sin iniciar')),
        (1, _('Esperando respuesta del evaluador')),
        (2, _('Finalizado')),
    )

    status = models.PositiveSmallIntegerField(
        _('Estado'),
        choices=STATUS_CHOICES,
        default=0
    )

    description = models.TextField(
        verbose_name=_(
            "Texto complementario a la respuesta"),
        help_text=_(
            "En caso de estar pegando desde el portapapeles asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 8000 caracteres considere incluirlo como una evidencia"
        ),
        max_length=10000,
        null=True,
        blank=True,
    )

    scope = models.ForeignKey(
        "questionnaires.Scope",
        verbose_name=_("Alcance"),
        related_name="question_tests",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.evaluation.ref} - {self.question.title}'

    class Meta:
        verbose_name = _("Respuesta")
        verbose_name_plural = _("Respuestas")

    def send_email_notification(self):
        from krm.configuration.models import Configuration

        configuration = Configuration.objects.first()

        # Esto notificará al control owner de que tiene controles por rellenar
        context = {
            "site_url": settings.SITE_URL,
            "recovery_url": settings.SITE_URL + reverse("auth:remember_password_form"),
            "user_email": self.evaluator.email,
            "evaluation_ref": self.evaluation.ref,
            "evaluation_questionnaire_ref": self.questionnaire.ref,
            "evaluation_questionnaire_name": self.questionnaire.name,
            "evaluation_date_begin": self.evaluation.date_begin,
            "evaluation_date_end": self.evaluation.date_end,
            "certification_year": self.evaluation.certification_year,
            "certification_period": self.evaluation.certification_period,
        }
        body_html = render_to_string(
            "emails/questionnaires/questionnaires_to_complete.html", context
        )
        context = {
            "content": body_html,
            "preheader": _("Cuestionario pendiente de completar"),
        }
        body_html = render_to_string("emails/base-inline.html", context)
        from_email = settings.EMAIL_FROM
        if settings.EMAIL_BCC:
            bcc = settings.EMAIL_BCC
        else:
            bcc = ""

        subject, from_email, to = (
            _("KRM Tool - Cuestionario de Compliance"),
            from_email,
            self.evaluator.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.evaluator.add_action(
            _("Envío de email de Test de Pregunta"))

        if configuration.enable_emails:
            return msg.send(fail_silently=False)
