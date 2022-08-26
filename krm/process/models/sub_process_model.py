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
        verbose_name=_("Identificador de subproceso"), max_length=140
    )

    name = models.CharField(verbose_name=_("Nombre"), max_length=500)

    description = models.TextField(
        _("Descripción"), max_length=10000, null=True, blank=True
    )

    process = models.ForeignKey(
        "process.Process",
        verbose_name=_("Proceso al que pertenece"),
        related_name="sub_processes",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sub Proceso")
        verbose_name_plural = _("Sub Procesos")
        ordering = ["process", "ref"]
        unique_together = ["process", "ref"]

    def save(self, *args, **kwargs):
        if not self.ref:
            max_ref = (
                SubProcess.objects.filter(process=self.process, ref__gte=0)
                .order_by("-ref")
                .first()
            )
            print(max_ref)
            if max_ref is not None and max_ref.ref is not None:
                self.ref = max_ref.ref + 1
            else:
                self.ref = 1
        super().save(*args, **kwargs)

    # @property
    # def get_controls(self):
    #     from krc.process.models import Control
    #     from django.db.models import Subquery

    #     return Control.objects.filter(risk__in=self.risks.all())

    # @property
    # def get_regulatory_frameworks(self):
    #     rfs = []
    #     for control in self.get_controls.all():
    #         for rf in control.regulatory_frameworks.all():
    #             rfs.append(rf)
    #     rfs = set(rfs)
    #     return rfs
