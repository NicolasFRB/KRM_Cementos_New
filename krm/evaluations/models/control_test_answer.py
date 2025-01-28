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

    CONTROL_RESULT_CHOICES = (
        ("EF", _("Efectivo")),
        ("SE", _("Sin establecer")),
        ("NE", _("No efectivo")),
        ("NA", _("No aplica en el periodo certificado")),
    )

    result = models.CharField(
        _("Resultado propuesto"),
        max_length=2,
        choices=CONTROL_RESULT_CHOICES,
        default="SE",
        null = True,
        blank = True
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

    @property
    def can_be_updated(self):
        from krm.configuration.models import Configuration
        # Si la configuración no permite actualizar respuestas devolvemos que no
        if Configuration.objects.get(pk=1).enable_delete_files_ct is False:
            return False
        # Si el control test está finalizado devolvemos que no
        if self.control_test.status == "FI":
            return False
        # Si la evaluación está finalizada devolvemos que no
        if self.control_test.evaluation.status == "FI":
            return False
        # Si no es la última respuesta para ese interlocutor, devolvemos que no
        if ControlTestAnswer.objects.filter(
            control_test=self.control_test,
            user=self.user
        ).order_by('-created').first() != self:
            return False

        # Si el control_Test no está esperando respuesta de ese usuario concreto


        return True
