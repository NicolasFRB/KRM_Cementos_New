from django.db import models

from django.utils.translation import gettext_lazy as _

from krm.utils.models import AuditModel


class DomainRisk(AuditModel):
    """Domain Risk model.
    Model for represent a Domain Risk
    """

    ref = models.CharField(
        verbose_name=_("Ref"),
        max_length=50,
        unique=True
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
        self.ref = self.ref
        super().save(*args, **kwargs)

        from krm.companies.models import Company
        from krm.companies.models import CompanyDomainRiskExperts, CompanyDomainRiskEvaluator
        for domain_risk in DomainRisk.objects.all():
            for company in Company.objects.all():
                if CompanyDomainRiskExperts.objects.filter(company=company, domain_risk=domain_risk).count() == 0:
                    CompanyDomainRiskExperts.objects.create(
                        company=company,
                        domain_risk=domain_risk
                    )
                if CompanyDomainRiskEvaluator.objects.filter(company=company, domain_risk=domain_risk).count() == 0:
                    CompanyDomainRiskEvaluator.objects.create(
                        company=company,
                        domain_risk=domain_risk
                    )

    @property
    def control_objects(self):
        controls = []
        for r1 in self.risks.all():
            for r2 in r1.risks.all():
                for c in r2.controls.all():
                    if c not in controls:
                        controls.append(c)

        return controls
