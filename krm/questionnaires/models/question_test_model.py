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

    def __str__(self):
        return f'{self.evaluation.ref} - {self.title}'

    class Meta:
        verbose_name = _("Respuesta")
        verbose_name_plural = _("Respuestas")
