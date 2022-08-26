from django.db import models

from django.utils.translation import gettext_lazy as _

from krm.utils.models import AuditModel


class Risk(AuditModel):
    """Risk model.
    Model for represent a Risk
    """

    ref = models.CharField(
        verbose_name=_("Ref"),
        max_length=50,
        blank=True,
        null=True,
    )

    name = models.CharField(
        verbose_name=_("Nombre"),
        max_length=140
    )

    description = models.TextField(
        _("Descripción"),
        max_length=10000
    )

    risk_master = models.ForeignKey(
        "risks.RiskMaster",
        verbose_name=_("Riesgo Maestro"),
        related_name="risks",
        on_delete=models.CASCADE,
    )

    IMPACT_RISK_CHOICES = (
        (1, _("Muy bajo")),
        (2, _("Bajo")),
        (3, _("Medio")),
        (4, _("Alto")),
        (5, _("Muy alto")),
    )

    impact_inherent = models.PositiveIntegerField(
        _("Impacto inherente"),
        choices=IMPACT_RISK_CHOICES,
        default=3
    )

    probability_inherent = models.PositiveIntegerField(
        _("Probabilidad inherente"),
        choices=IMPACT_RISK_CHOICES,
        default=3
    )

    impact_residual = models.PositiveIntegerField(
        _("Impacto residual"),
        choices=IMPACT_RISK_CHOICES,
        default=3
    )

    probability_residual = models.PositiveIntegerField(
        _("Probabilidad residual"),
        choices=IMPACT_RISK_CHOICES,
        default=3
    )

    # controls =

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Riesgo")
        verbose_name_plural = _("Riesgos")
        ordering = ["risk_master", "ref", "name"]

    def save(self, *args, **kwargs):
        if not self.ref:
            max_ref = Risk.objects.all().count()
            if max_ref > 0:
                self.ref = max_ref + 1
            else:
                self.ref = 1
        super().save(*args, **kwargs)
