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
    path = "control_test_answer/"
    name = filename.replace(" ", "_").lower()
    name = slugify(name)
    format = (
        path
        + str(instance.control_test.pk)
        + "_"
        + urllib.parse.quote(name)
        + Path(filename).suffix
    )

    return format


class ControlTestAnswer(AuditModel):
    """ControlTestAnswer model.
    Modelo que usaremos para representar una respuesta a un Test de control
    """

    control_test = models.ForeignKey(
        "evaluations.ControlTest",
        verbose_name=_("Test de Control"),
        related_name="answers",
        on_delete=models.CASCADE,
    )

    description = models.TextField(
        verbose_name=_(
            "Comentarios de la realización o supervisión del control"),
        help_text=_(
            "En caso de estar pegando desde el portapapeles asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 8000 caracteres considere incluirlo como una evidencia"
        ),
        max_length=10000,
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        "users.User",
        verbose_name=_("Autor de la respuesta"),
        related_name="control_test_answers",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    attachment_1 = models.FileField(
        verbose_name=_("Archivo adjunto 1"),
        help_text=_("Tamaño máximo de archivo de 50MB"),
        upload_to=update_filename,
        validators=[validate_file_size],
        blank=True,
        null=True,
    )

    attachment_2 = models.FileField(
        verbose_name=_("Archivo adjunto 2"),
        help_text=_("Tamaño máximo de archivo de 50MB"),
        upload_to=update_filename,
        validators=[validate_file_size],
        blank=True,
        null=True,
    )

    attachment_3 = models.FileField(
        verbose_name=_("Archivo adjunto 3"),
        help_text=_("Tamaño máximo de archivo de 50MB"),
        upload_to=update_filename,
        validators=[validate_file_size],
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = _("Respuesta a un Test de Control")
        verbose_name_plural = _("Respuestas a un Test de Control")
        ordering = (
            "control_test",
            "created",
        )

    @property
    def description_safe(self):
        return str(strip_tags(self.description))
