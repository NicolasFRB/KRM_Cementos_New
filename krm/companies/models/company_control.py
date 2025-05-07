# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel


class CompanyControls(AuditModel):

    active = models.BooleanField(
        _("Activo"),
        default=False
    )

    company = models.ForeignKey(
        'companies.Company',
        related_name='company_controls',
        on_delete=models.CASCADE
    )

    control = models.ForeignKey(
        'controls.Control',
        on_delete=models.CASCADE
    )

    control_test_owners = models.ManyToManyField(
        "users.User",
        verbose_name=_("Cumplimentadores del Control (Control Owner)"),
        related_name="company_controls_owners",
        blank=True,
    )

    control_test_supervisors = models.ManyToManyField(
        "users.User",
        verbose_name=_("Supervisores del Control (Control Supervisor)"),
        related_name="company_controls_supervisors",
        blank=True,
    )

    def __str__(self):
        return f'{self.company.name} - {self.control.ref}'

    class Meta:
        verbose_name = _("Control para Compañías")
        verbose_name_plural = _("Controles para compañías")
        ordering = ["company", "control"]
