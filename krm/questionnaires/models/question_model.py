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
        max_length=2000,
    )

    questionnaire = models.ForeignKey(
        "questionnaires.Questionnaire",
        verbose_name=_("Cuestionario"),
        on_delete=models.CASCADE,
        related_name='questions'
    )

    delegation = models.CharField(
        verbose_name=_("Delegación"),
        max_length=200,
        blank=True,
        null=True
    )

    concession = models.CharField(
        verbose_name=_("Concesión"),
        max_length=200,
        blank=True,
        null=True
    )

    area = models.CharField(
        verbose_name=_("Área"),
        max_length=200,
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(
        verbose_name=_("Número de pregunta dentro del cuestionario"),
        default=1
    )

    title = models.TextField(
        verbose_name=_("Enunciado"),
        max_length=5000
    )

    user_to_assign = models.ManyToManyField(
        'users.User',
        verbose_name=_('Posibles respondedores'),
        blank=True,
        related_name='questions_to_assign'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Pregunta")
        verbose_name_plural = _("Preguntas")
        ordering = ['questionnaire', 'order']
