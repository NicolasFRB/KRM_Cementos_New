"""ControlTest model."""

import random

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import translation

# Utilities
from krm.utils.models import AuditModel
from krm.risks.models import DomainRisk

from krm.configuration.models import Configuration


class ControlTest(AuditModel):
    """ControlTest model.
    Modelo que usaremos para representar un test de control
    """

    evaluation = models.ForeignKey(
        "evaluations.evaluation",
        verbose_name=_("Evaluación"),
        related_name="control_tests",
        on_delete=models.CASCADE,
    )

    control = models.ForeignKey(
        "controls.Control",
        related_name="control_tests", on_delete=models.CASCADE
    )

    date_begin = models.DateField(
        verbose_name=_(u"Fecha en la que comenzará el Test de Control"),
    )

    control_test_supervisor = models.ForeignKey(
        "users.User",
        verbose_name=_("Supervisor del Test de Control"),
        related_name="controls_test_supervisor",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    control_test_owner = models.ForeignKey(
        "users.User",
        verbose_name=_("Cumplimentador del Test de Control (Control Owner)"),
        related_name="controls_test_owner",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    CONTROL_STATUS_CHOICES = (
        ("SI", _("Sin iniciar")),
        ("WO", _("En espera de respuesta del Control Owner")),
        ("WS", _("En espera de respuesta del Control Supervisor")),
        ("WA", _("En espera de respuesta del Control Administrator")),
        ("FI", _("Finalizado")),
    )

    status = models.CharField(
        _("Estado del test de control"),
        max_length=2,
        choices=CONTROL_STATUS_CHOICES,
        default="SI",
    )

    CONTROL_RESULT_CHOICES = (
        ("EF", _("Efectivo")),
        ("SE", _("Sin establecer")),
        ("NE", _("No efectivo")),
        ("NA", _("N/A")),
    )

    result = models.CharField(
        _("Resultado del test de control"),
        max_length=2,
        choices=CONTROL_RESULT_CHOICES,
        default="SE",
    )

    remediation_plan_needed = models.BooleanField(
        _('¿Es necesario un plan de remediación?'),
        default=False
    )

    def __str__(self):
        return self.identifier

    class Meta:
        verbose_name = _("Test de Control")
        verbose_name_plural = _("Tests de Controles")

    @property
    def identifier(self):
        return str(self.control.ref).zfill(4)
        # return str(self.process_test.identifier) + '-' + str(self.control.ref).zfill(4)

    def get_control_test_risks_company(self):
        risks_company = self.evaluation.company.krm_risks.filter(active=True)
        risks_control = self.control.risks.all()
        return risks_company.filter(risk__in=risks_control)

    def get_control_test_domain_risks(self):
        r_company = self.get_control_test_risks_company()
        domain_risks_pk = []

        for r in r_company:
            dom_risk_pk = r.risk.risk_master.domain_risk.pk
            if dom_risk_pk not in domain_risks_pk:
                domain_risks_pk.append(dom_risk_pk)

        return DomainRisk.objects.filter(id__in=domain_risks_pk)

    def get_control_test_subprocess(self):
        return self.control.sub_processes.all()

    def send_notification(self, notif_type):
        from krm.evaluations.tasks import (
            control_test_send_notification_control_owner,
            control_test_send_notification_control_supervisor
        )

        # Ahora para mandar las notificaciones comprobamos a quien corresponde
        if self.result in ("FI", "SI"):
            return

        if self.status == "WO":
            control_test_send_notification_control_owner.delay(self.pk, notif_type)

        elif self.status == "WS":
            control_test_send_notification_control_supervisor.delay(self.pk, notif_type)

    def sent_notification_control_owner(self, notif_type):
        from krm.configuration.models import Configuration

        configuration = Configuration.objects.first()

        translation.activate(self.control_test_owner.notification_language)

        # Esto notificará al control owner de que tiene controles por rellenar
        if self.evaluation.certification_period:
            period = " (%s)" % self.evaluation.certification_period
        else:
            period = ""
        context = {
            "site_url": settings.SITE_URL,
            "recovery_url": settings.SITE_URL + reverse("auth:remember_password_form"),
            "user_email": self.control_test_owner.email,
            "evaluation_ref": self.evaluation.ref,
            "evaluation_date_begin": self.evaluation.date_begin,
            "evaluation_date_intermediate": self.evaluation.date_intermediate,
            "certification_year": self.evaluation.certification_year,
            "certification_period": period,
            "ncontrols_pending": self.evaluation.ncontrols_test_by_state("WO", user=self.control_test_owner, rol='control_test_owner'),
            "app_name": configuration.app_name,
            "notif_type": notif_type,
        }
        body_html = render_to_string(
            "emails/control_test/control_test_notification_control_owner.html", context
        )
        context = {
            "content": body_html,
            "preheader": _("Controles pendientes de completar"),
            "BRAND": settings.BRAND,
            "app_name": configuration.app_name,
        }
        body_html = render_to_string("emails/base-inline.html", context)
        from_email = settings.EMAIL_FROM
        if settings.EMAIL_BCC:
            bcc = settings.EMAIL_BCC
        else:
            bcc = ""

        subject, from_email, to = (
            _("{} - Evaluación de controles de Compliance".format(configuration.app_name)),
            from_email,
            self.control_test_owner.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.control_test_owner.add_action(
            _("[%s] Envío de email de Controles pendientes de completar (COwner) (%s)" % (notif_type.upper(), self.evaluation.ref)))

        if configuration.enable_emails:
            msg.send(fail_silently=False)

    def sent_notification_control_supervisor(self, notif_type):
        from krm.configuration.models import Configuration

        configuration = Configuration.objects.first()
        translation.activate(
            self.control_test_supervisor.notification_language)

        # Esto notificará al control supervisor de que tiene controles por supervisar
        if self.evaluation.certification_period:
            period = " (%s)" % self.evaluation.certification_period
        else:
            period = ""
        context = {
            "site_url": settings.SITE_URL,
            "recovery_url": settings.SITE_URL + reverse("auth:remember_password_form"),
            "user_email": self.control_test_supervisor.email,
            "evaluation_ref": self.evaluation.ref,
            "evaluation_date_begin": self.evaluation.date_begin,
            "evaluation_date_end": self.evaluation.date_end,
            "certification_year": self.evaluation.certification_year,
            "certification_period": period,
            "ncontrols_pending": self.evaluation.ncontrols_test_by_state("WS", user=self.control_test_supervisor, rol='control_test_supervisor'),
            "app_name": configuration.app_name,
            "notif_type": notif_type,
        }
        body_html = render_to_string(
            "emails/control_test/control_test_notification_control_supervisor.html",
            context,
        )
        context = {
            "content": body_html,
            "preheader": _("Controles pendientes de supervisar"),
            "BRAND": settings.BRAND,
            "app_name": configuration.app_name,
        }
        body_html = render_to_string("emails/base-inline.html", context)
        from_email = settings.EMAIL_FROM
        if settings.EMAIL_BCC:
            bcc = settings.EMAIL_BCC
        else:
            bcc = ""

        subject, from_email, to = (
            _("{} - Evaluación de controles de Compliance".format(configuration.app_name)),
            from_email,
            self.control_test_supervisor.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.control_test_supervisor.add_action(
            _("[%s] Envío de email de Controles pendientes de supervisar (CSupervisor) (%s)" % (notif_type.upper(), self.evaluation.ref)))
        if configuration.enable_emails:
            msg.send(fail_silently=False)
