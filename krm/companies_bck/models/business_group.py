# Django
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.utils import translation
from django.db.models import Count

from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse

from django_countries.fields import CountryField

# Utilities
from krc.utils.models import KrcModel
from krc.users.models import User


class BusinessGroup(KrcModel):
    """BusinessGroup model.

    Modelo que usaremos para representar un grupo empresarial
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

    email = models.EmailField(
        _("Email"),
        blank=True,
        null=True,
        unique=True,
        error_messages={"unique": _(
            "Dicho email ya está en uso por otro cliente.")},
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Grupo empresarial")
        verbose_name_plural = _("Grupos empresariales")
        ordering = ["name"]

    def get_users(self):
        from krc.users.models import User

        return User.objects.filter(companies__in=self.companies.all(), is_active=True)

    def get_process_tests(self):
        from krc.process_test.models import ProcessTest

        return ProcessTest.objects.filter(company__in=self.companies.all())

    def get_control_tests(self):
        from krc.process_test.models import ControlTest

        return ControlTest.objects.filter(process_test__in=self.get_process_tests())

    def get_process_tests_status_aggregate(self):
        from krc.process_test.models import ProcessTest
        from krc.utils import COLORS

        process = (
            ProcessTest.objects.filter(company__in=self.companies.all())
            .values("status")
            .annotate(num_proces_tests=Count("id"))
        )
        gd_process = []
        for c in process:
            e = {}
            e["label"] = COLORS[c["status"]]["label"]
            e["color"] = COLORS[c["status"]]["color"]
            e["data"] = c["num_proces_tests"]
            gd_process.append(e)

        return gd_process

    def get_control_tests_status_aggregate(self):
        from krc.process_test.models import ControlTest
        from krc.utils import COLORS

        controls = (
            ControlTest.objects.filter(
                process_test__in=self.get_process_tests())
            .values("status")
            .annotate(num_controls=Count("id"))
        )
        gd_controls = []
        for c in controls:
            e = {}
            e["label"] = COLORS[c["status"]]["label"]
            e["color"] = COLORS[c["status"]]["color"]
            e["data"] = c["num_controls"]
            gd_controls.append(e)

        return gd_controls

    def get_control_tests_result_aggregate(self):
        from krc.process_test.models import ControlTest
        from krc.utils import COLORS

        controls = (
            ControlTest.objects.filter(
                process_test__in=self.get_process_tests())
            .values("result")
            .annotate(num_controls=Count("id"))
        )
        gd_controls = []
        for c in controls:
            e = {}
            e["label"] = COLORS[c["result"]]["label"]
            e["color"] = COLORS[c["result"]]["color"]
            e["data"] = c["num_controls"]
            gd_controls.append(e)

        return gd_controls
