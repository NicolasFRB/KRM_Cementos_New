from django.db import models

from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from krm.utils.models import AuditModel


class RiskMaster(AuditModel):
    """Risk Master model.
    Model for represent a Risk Master
    """

    ref = models.CharField(
        verbose_name=_("REF"),
        max_length=50,
        unique=True
    )

    name = models.CharField(
        verbose_name=_("Nombre"),
        max_length=140
    )

    description = RichTextField(
        _("Descripción"),
        config_name='awesome_ckeditor',
        max_length=10000
    )

    domain_risk = models.ForeignKey(
        "risks.DomainRisk",
        verbose_name=_("Dominio de Riesgo"),
        related_name="risks",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("Riesgo Maestro")
        verbose_name_plural = _("Riesgos Maestros")
        ordering = ["domain_risk", "name"]

    def save(self, *args, **kwargs):
        self.ref = self.ref
        super().save(*args, **kwargs)
