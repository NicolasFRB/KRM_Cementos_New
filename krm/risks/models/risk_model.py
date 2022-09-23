from django.db import models

from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

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

    description = RichTextField(
        _("Descripción"),
        config_name='awesome_ckeditor',
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

    krm_activity_affected = RichTextField(
        _("Actividad afectada"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True
    )

    krm_main_events = RichTextField(
        _("Describa los principales eventos en los que el riesgo se materializa o se espera que se materialice. Comentarios"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True
    )

    krm_exposed_staff = RichTextField(
        _("Personal especialmente expuesto al Riesgo"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True
    )

    krm_main_elements = RichTextField(
        _("Principales elementos del Riesgo"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Riesgo")
        verbose_name_plural = _("Riesgos")
        ordering = ["risk_master", "name"]

    def save(self, *args, **kwargs):
        self.ref = self.ref.upper()
        super().save(*args, **kwargs)
