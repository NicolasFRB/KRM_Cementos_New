from django.db import models

from django.utils.translation import gettext_lazy as _

from krm.utils.models import AuditModel


class DomainRisk(AuditModel):
    """Domain Risk model.
    Model for represent a Domain Risk
    """

    ref = models.CharField(
        verbose_name=_("Ref"),
        max_length=50
    )

    name = models.CharField(
        verbose_name=_("Nombre"),
        max_length=140
    )

    description = models.TextField(
        verbose_name=_("Descripción"),
        max_length=10000
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Dominio de Riesgo")
        verbose_name_plural = _("Dominios de Riesgo")
        ordering = ["ref", "name"]

    def save(self, *args, **kwargs):
        if not self.ref:
            max_ref = DomainRisk.objects.all().count()
            if max_ref > 0:
                self.ref = max_ref + 1
            else:
                self.ref = 1
        super().save(*args, **kwargs)
