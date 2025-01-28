"""RemediationPlan model."""

import urllib
from pathlib import Path

# Django
from django.utils.text import slugify
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import translation

# Utilities
from krm.utils.models import AuditModel


def update_filename(instance, filename):
    path = "remediation_plan/"
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


# class RemediationPlan(AuditModel):
#     """RemediationPlan model.
#     Modelo que usaremos para representar un plan de remediación para un test de control no efectivo
#     """

#     control_test = models.ForeignKey(
#         "evaluations.ControlTest",
#         related_name="remediation_plans",
#         on_delete=models.CASCADE,
#     )

#     description = models.TextField(
#         _("Descripción del plan de remediación"), max_length=10000
#     )

#     date_end = models.DateField(
#         verbose_name=_(u"Fecha de vencimiento del Plan de Remediación"),
#     )

#     attachment = models.FileField(
#         verbose_name=_("Archivo adjunto"),
#         upload_to=update_filename,
#         blank=True,
#         null=True,
#     )

#     user = models.ForeignKey(
#         "users.User",
#         verbose_name=_("Creador del Plan de Remediación"),
#         related_name="remediaton_plans",
#         blank=True,
#         null=True,
#         on_delete=models.CASCADE,
#     )

#     STATUS_CHOICES = (
#         ("AC", _("Activo")),
#         ("VE", _("Vencido")),
#     )

#     status = models.CharField(
#         _("Estado"), max_length=2, choices=STATUS_CHOICES, default="AC"
#     )

#     class Meta:
#         verbose_name = _("Plan de remediación")
#         verbose_name_plural = _("Planes de remediación")
