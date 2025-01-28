"""ControlTestAnswer model."""

import urllib
from pathlib import Path

# Django
from django.utils.text import slugify
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.utils.html import strip_tags

# Utilities
from krm.utils.models import AuditModel

from krm.evaluations.validators import validate_file_size


def update_filename(instance, filename):
    path = "remediation_plan/"
    name = filename.replace(" ", "_").lower()
    name = slugify(name)
    format = (
        path
        + str(instance.remediation_plan.pk)
        + "_"
        + urllib.parse.quote(name)
        + Path(filename).suffix
    )

    return format


class RemediationPlanAnswer(AuditModel):

    remediation_plan = models.ForeignKey(
        "remediation_plans.RemediationPlan",
        verbose_name=_("Plan de Remediación"),
        related_name="answers",
        on_delete=models.CASCADE,
    )

    description = models.TextField(
        verbose_name=_(
            "Comentarios del seguimiento del plan de remediación"),
        help_text=_(
            "En caso de estar pegando desde el portapapeles asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 8000 caracteres considere incluirlo como una evidencia"
        ),
        max_length=10000
    )

    user = models.ForeignKey(
        "users.User",
        verbose_name=_("Autor de la respuesta"),
        related_name="remediation_plan_answers",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    attachment_1 = models.FileField(
        verbose_name=_("Archivo adjunto"),
        help_text=_("Tamaño máximo de archivo de 50MB"),
        upload_to=update_filename,
        validators=[validate_file_size],
        blank=True,
        null=True,
    )

    status = models.CharField(
        _("Estado"),
        max_length=2,
        choices=(
            ("EP", _("En progreso")),
            ("CO", _("Completado")),
        ),
        default="EP",
    )

    REMEDIATION_PLAN_STATUS_CHOICES = (
        ("WR", _("Responsable")),
        ("WS", _("Supervisor")),
        ("FI", _("Finalizado")),
    )

    next_to_reply = models.CharField(
        _("¿Quien debe responder?"),
        max_length=2,
        choices=REMEDIATION_PLAN_STATUS_CHOICES,
        default="WR",
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = _("Respuesta a un Plan de Remediación")
        verbose_name_plural = _("Respuestas a un Plan de Remediación")
        ordering = (
            "remediation_plan",
            "created",
        )

    @property
    def description_safe(self):
        return str(strip_tags(self.description))
