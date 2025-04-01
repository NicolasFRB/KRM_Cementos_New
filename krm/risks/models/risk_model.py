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
        max_length=10000,
        blank=True,
        null=True
    )

    risk_master = models.ForeignKey(
        "risks.RiskMaster",
        verbose_name=_("Riesgo Maestro"),
        related_name="risks",
        on_delete=models.CASCADE,
    )

    IMPACT_RISK_CHOICES = (
        (0, _('Sin establecer')),
        (1, _("Muy bajo")),
        (2, _("Bajo")),
        (3, _("Medio")),
        (4, _("Alto")),
        (5, _("Muy alto")),
    )

    PROBABILITY_RISK_CHOICES= (
        (1, _("Remoto")),
        (2, _("Posible")),
        (3, _("Probable")),
        (4, _("Muy probable")),
        (5, _("Prácticamente cierto")),
    )

    EVENT_SPEED_RISK_CHOICES= (
        (0, _('Sin establecer')),
        (1, _("Muy baja")),
        (2, _("Baja")),
        (3, _("Media")),
        (4, _("Alta")),
        (5, _("Muy alta")),
    )

    impact_inherent = models.PositiveIntegerField(
        _("Impacto inherente"),
        choices=IMPACT_RISK_CHOICES,
        default=0
    )

    probability_inherent = models.PositiveIntegerField(
        _("Probabilidad inherente"),
        choices=PROBABILITY_RISK_CHOICES,
        default=3
    )

    impact_residual = models.PositiveIntegerField(
        _("Impacto residual"),
        choices=IMPACT_RISK_CHOICES,
        default=0
    )

    probability_residual = models.PositiveIntegerField(
        _("Probabilidad residual"),
        choices=PROBABILITY_RISK_CHOICES,
        default=3
    )

    event_speed= models.PositiveIntegerField(
        _("Velocidad de ocurrencia"),
        choices=EVENT_SPEED_RISK_CHOICES,
        default=0
    )

    krm_activity_affected = RichTextField(
        _("Actividad afectada"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True,
        null=True
    )

    krm_main_events = RichTextField(
        _("Describa los principales eventos en los que el riesgo se materializa o se espera que se materialice. Comentarios"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True,
        null=True
    )

    krm_exposed_staff = RichTextField(
        _("Personal especialmente expuesto al Riesgo"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True,
        null=True
    )

    krm_main_elements = RichTextField(
        _("Principales elementos del Riesgo"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Riesgo")
        verbose_name_plural = _("Riesgos")
        ordering = ["risk_master", "name"]

    @property
    def risk_master_name(self):
        return self.risk_master.name

    def save(self, *args, **kwargs):
        self.ref = self.ref.upper()
        super().save(*args, **kwargs)

        from krm.companies.models import Company
        from krm.risks.models import RiskCompany

        for company in Company.objects.all():
            if RiskCompany.objects.filter(
                company=company,
                risk=self
            ).count() == 0:
                RiskCompany.objects.create(
                    company=company,
                    risk=self,
                    name=self.name,
                    description=self.description,
                    krm_activity_affected=self.krm_activity_affected,
                    krm_main_events=self.krm_main_events,
                    krm_exposed_staff=self.krm_exposed_staff,
                    krm_main_elements=self.krm_main_elements
                )
