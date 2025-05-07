# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel


class CompanyDomainRiskExperts(AuditModel):

    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE
    )

    domain_risk = models.ForeignKey(
        'risks.Domainrisk',
        on_delete=models.CASCADE
    )

    expert = models.ForeignKey(
        'users.User',
        verbose_name=_('Experto asignado'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        if self.expert:
            return f'{self.company.name} - {self.domain_risk.ref} - {self.expert.email}'
        else:
            return f'{self.company.name} - {self.domain_risk.ref}'

    class Meta:
        verbose_name = _("Experto de Dominio de Riesgo para Compañía")
        verbose_name_plural = _(
            "Expertos de Dominios de Riesgo para Compañías")
        ordering = ["company", "domain_risk"]
