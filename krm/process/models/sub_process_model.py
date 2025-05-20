# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel


class SubProcess(AuditModel):
    """SubProcess model.
    Modelo que usaremos para representar un subproceso
    """

    ref = models.CharField(
        _("Identificador de subproceso"),
        max_length=140,
        unique=True
    )

    name = models.CharField(
        ("Nombre"),
        max_length=500
    )

    description = models.TextField(
        _("Descripción"),
        max_length=10000,
        null=True,
        blank=True
    )

    process = models.ForeignKey(
        "process.Process",
        verbose_name=_("Proceso al que pertenece"),
        related_name="sub_processes",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("Sub Proceso")
        verbose_name_plural = _("Sub Procesos")
        ordering = ["process", "ref"]
        unique_together = ["process", "ref"]

    def save(self, *args, **kwargs):
        self.ref = self.ref.upper()
        super().save(*args, **kwargs)
