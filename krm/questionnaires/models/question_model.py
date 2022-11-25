"""Booking model."""
import os
import hashlib
import random
from tabnanny import verbose

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel


class Question(AuditModel):
    """Question model.
    Modelo que usaremos para representar una pregunta
    """

    ref = models.CharField(
        verbose_name=_("Ref"),
        max_length=50,
        unique=True
    )

    questionnaire = models.ForeignKey(
        "questionnaires.Questionnaire",
        verbose_name=_("Cuestionario"),
        on_delete=models.CASCADE,
        related_name='questions'
    )

    order = models.PositiveIntegerField(
        verbose_name=_("Número de pregunta dentro del cuestionario"),
        default=1
    )

    title = models.CharField(
        verbose_name=_("Enunciado"),
        max_length=200
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Pregunta")
        verbose_name_plural = _("Preguntas")
        ordering = ['questionnaire', 'order']
