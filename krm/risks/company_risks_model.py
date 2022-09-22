from django.db import models

from django.utils.translation import gettext_lazy as _

from krm.utils.models import AuditModel


class Risk(AuditModel):
    """Risk model.
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

    description = models.TextField(
        _("Descripción"),
        max_length=10000
    )

    domain_risk = models.ForeignKey(
        "risks.DomainRisk",
        verbose_name=_("Dominio de Riesgo"),
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

    # IMPACT_RISK_CHOICES = (
    #     (1, _("Muy bajo")),
    #     (2, _("Bajo")),
    #     (3, _("Medio")),
    #     (4, _("Alto")),
    #     (5, _("Muy alto")),
    # )

    # impact = models.PositiveIntegerField(_("Impacto"), choices=IMPACT_RISK_CHOICES)

    # probability = models.PositiveIntegerField(
    #     _("Probabilidad"), choices=IMPACT_RISK_CHOICES
    # )

    # rating = models.PositiveIntegerField(
    #     _("Rating"), blank=True, null=True, choices=IMPACT_RISK_CHOICES
    # )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Riesgo")
        verbose_name_plural = _("Riesgos")
        ordering = ["domain_risk", "name"]

    def save(self, *args, **kwargs):
        if not self.ref:
            max_ref = Risk.objects.filter(
                domain_risk__pk=self.domain_risk.pk).count()
            max_ref = max_ref + 1
            max_ref = str(max_ref).zfill(3)
            self.ref = f"{self.domain_risk.ref}{max_ref}"
        super().save(*args, **kwargs)
