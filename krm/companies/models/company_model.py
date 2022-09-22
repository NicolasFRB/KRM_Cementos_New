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
        _("Dirección"), max_length=140, null=True, blank=True)

    state = models.CharField(
        _("Población"), max_length=140, null=True, blank=True)

    cp = models.PositiveIntegerField(_("Código Postal"), null=True, blank=True)

    country = CountryField(_("País"), null=True, blank=True)

    email = models.EmailField(_("Email"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sociedad")
        verbose_name_plural = _("Sociedades")
        ordering = ["name"]

    @property
    def experts_domain_risk(self):
        from krm.companies.models import CompanyDomainRiskExperts
        return CompanyDomainRiskExperts.objects.filter(company=self)

    # @property
    # def employees_active(self):
    #     return self.employees.filter(is_active=True)

    # def get_control_tests(self):
    #     from krc.process_test.models import ControlTest

    #     return ControlTest.objects.filter(process_test__in=self.process_tests.all())

    # def get_process_tests_status_aggregate(self):
    #     from krc.process_test.models import ProcessTest
    #     from krc.utils import COLORS

    #     process = (
    #         self.process_tests.all()
    #         .values("status")
    #         .annotate(num_proces_tests=Count("id"))
    #     )
    #     gd_process = []
    #     for c in process:
    #         e = {}
    #         e["label"] = COLORS[c["status"]]["label"]
    #         e["color"] = COLORS[c["status"]]["color"]
    #         e["data"] = c["num_proces_tests"]
    #         gd_process.append(e)

    #     return gd_process

    # def get_control_tests_status_aggregate(self):
    #     from krc.process_test.models import ControlTest
    #     from krc.utils import COLORS

    #     controls = (
    #         ControlTest.objects.filter(process_test__in=self.process_tests.all())
    #         .values("status")
    #         .annotate(num_controls=Count("id"))
    #     )
    #     gd_controls = []
    #     for c in controls:
    #         e = {}
    #         e["label"] = COLORS[c["status"]]["label"]
    #         e["color"] = COLORS[c["status"]]["color"]
    #         e["data"] = c["num_controls"]
    #         gd_controls.append(e)

    #     return gd_controls

    # def get_control_tests_result_aggregate(self):
    #     from krc.process_test.models import ControlTest
    #     from krc.utils import COLORS

    #     controls = (
    #         ControlTest.objects.filter(process_test__in=self.process_tests.all())
    #         .values("result")
    #         .annotate(num_controls=Count("id"))
    #     )
    #     gd_controls = []
    #     for c in controls:
    #         e = {}
    #         e["label"] = COLORS[c["result"]]["label"]
    #         e["color"] = COLORS[c["result"]]["color"]
    #         e["data"] = c["num_controls"]
    #         gd_controls.append(e)

    #     return gd_controls
