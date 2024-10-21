from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel

# Create your models here.
class RemediationPlan(AuditModel):

    date_begin = models.DateField(
        verbose_name=_("Fecha inicio"),
    )

    date_end = models.DateField(
        verbose_name=_("Fecha fin"),
    )

    responsible = models.ForeignKey(
        'users.User',
        verbose_name=_('Usuario responsable'),
        on_delete=models.CASCADE,
        related_name='rp_responsible',
        blank=True,
        null=True
    )

    supervisor = models.ForeignKey(
        'users.User',
        verbose_name=_('Usuario supervisor'),
        on_delete=models.CASCADE,
        related_name='rp_supervisor',
        blank=True,
        null=True
    )

    additional_users = models.ManyToManyField(
        'users.User',
        verbose_name=_('Usuarios adicionales'),
        blank=True
    )

    description = models.TextField(
        verbose_name=_("Descripción"),
        max_length=10000,
        blank=True,
        null=True
    )

    STATUS_CHOICES = (
        ("EP", _("En progreso")),
        ("CO", _("Completado")),
    )

    status = models.CharField(
        _("Estado"),
        max_length=2,
        choices=STATUS_CHOICES,
        default="EP",
    )

    control = models.ForeignKey(
        'controls.Control',
        verbose_name=_('Control'),
        on_delete=models.CASCADE,
        related_name='rp_control',
        blank=True,
        null=True
    )

    control_test = models.ForeignKey(
        'evaluations.ControlTest',
        verbose_name=_('Test de control'),
        on_delete=models.CASCADE,
        related_name='rp_control_test',
        blank=True,
        null=True
    )

    REMEDIATION_PLAN_STATUS_CHOICES = (
        ("WR", _("Responsable")),
        ("WS", _("Supervisor")),
        ("FI", _("Finalizado")),
    )

    next_to_reply = models.CharField(
        _("¿Quien debe responder?"),
        max_length=2,
        choices=REMEDIATION_PLAN_STATUS_CHOICES,
        default="WR",
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = _("Plan de remediación")
        verbose_name_plural = _("Planes de remediación")
