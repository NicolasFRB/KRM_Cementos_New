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


class Questionnaire(AuditModel):
    """Questionnaire model.
    Modelo que usaremos para representar un cuestionario
    """

    ref = models.CharField(
        verbose_name=_("Ref"),
        max_length=50,
        unique=True
    )

    name = models.CharField(verbose_name=_("Nombre"), max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Cuestionario")
        verbose_name_plural = _("Cuestionarios")
        ordering = ["name"]
