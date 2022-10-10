"""Booking model."""
import os
import hashlib
import random

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

# Utilities
from krm.utils.models import AuditModel


class Company(AuditModel):
    """Company model.

    Modelo que usaremos para representar una compañía
    """

    ref = models.CharField(
        verbose_name=_("Ref"),
        max_length=50,
        unique=True
    )

    name = models.CharField(verbose_name=_("Nombre"), max_length=200)

    vat = models.CharField(
        _("CIF"),
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        error_messages={"unique": _("Dicho Vat ya está en uso.")},
    )

    address = models.CharField(
        _("Dirección"),
        max_length=140,
        null=True,
        blank=True
    )

    state = models.CharField(
        _("Población"),
        max_length=140,
        null=True,
        blank=True
    )

    cp = models.PositiveIntegerField(_("Código Postal"),
                                     null=True,
                                     blank=True
                                     )

    country = CountryField(_("País"),
                           null=True,
                           blank=True
                           )

    email = models.EmailField(_("Email"),
                              blank=True,
                              null=True
                              )

    type_company = models.CharField(
        _("Tipo"),
        max_length=200,
        null=True,
        blank=True
    )

    companies_in_scope = models.CharField(
        "Companies in scope",
        max_length=1000,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Compañía")
        verbose_name_plural = _("Compañía")
        ordering = ["ref", "name"]

    @property
    def experts_domain_risk(self):
        from krm.companies.models import CompanyDomainRiskExperts
        return CompanyDomainRiskExperts.objects.filter(company=self)

    @property
    def evaluators_domain_risk(self):
        from krm.companies.models import CompanyDomainRiskEvaluator
        return CompanyDomainRiskEvaluator.objects.filter(company=self)

    @property
    def krm_risks_active(self):
        return self.krm_risks.filter(active=True)

    def save(self, *args, **kwargs):
        self.ref = self.ref.upper()
        super().save(*args, **kwargs)

        from krm.companies.models import CompanyDomainRiskExperts, CompanyDomainRiskEvaluator
        from krm.risks.models import DomainRisk, Risk, RiskCompany

        for domain_risk in DomainRisk.objects.all():
            if CompanyDomainRiskExperts.objects.filter(company=self, domain_risk=domain_risk).count() == 0:
                CompanyDomainRiskExperts.objects.create(
                    company=self,
                    domain_risk=domain_risk
                )
            if CompanyDomainRiskEvaluator.objects.filter(company=self, domain_risk=domain_risk).count() == 0:
                CompanyDomainRiskEvaluator.objects.create(
                    company=self,
                    domain_risk=domain_risk
                )
        for risk in Risk.objects.all():
            if RiskCompany.objects.filter(company=self, risk=risk).count() == 0:
                RiskCompany.objects.create(
                    company=self,
                    risk=risk
                )
