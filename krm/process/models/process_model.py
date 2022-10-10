from django.db import models

import datetime

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from django.conf import settings

# Utilities
from krm.utils.models import AuditModel


class Process(AuditModel):
    """Process model.
    Modelo que usaremos para representar un proceso
    """

    ref = models.CharField(
        _("REF"),
        max_length=140,
        unique=True
    )

    name = models.CharField(verbose_name=_("Nombre"), max_length=500)

    description = models.TextField(
        _("Descripción"), max_length=10000, null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Proceso")
        verbose_name_plural = _("Procesos")
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.ref = self.ref.upper()
        super().save(*args, **kwargs)
