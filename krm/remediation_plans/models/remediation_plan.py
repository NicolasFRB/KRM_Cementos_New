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
        max_length=10000
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

    control = models.ManyToManyField(
        'controls.Control',
        verbose_name=_('Controles'),
        related_name='rp_control',
        blank=True
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
        _("¿Quién debe responder?"),
        max_length=2,
        choices=REMEDIATION_PLAN_STATUS_CHOICES,
        default="WR",
    )

    company = models.ForeignKey(
      'companies.Company',
      verbose_name=_('Compañía'),
      on_delete=models.CASCADE,
      related_name='remediation_plans',
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = _("Plan de remediación")
        verbose_name_plural = _("Planes de remediación")

    def get_domain_risks(self):
        domain_risks = []
        for control in self.control.all():
            for risk in control.risks.all():
                if risk.risk_master.domain_risk.pk not in domain_risks:
                    domain_risks.append(risk.risk_master.domain_risk.pk)
        if self.control_test:
            for risk in self.control_test.control.risks.all():
                if risk.risk_master.domain_risk.pk not in domain_risks:
                    domain_risks.append(risk.risk_master.domain_risk.pk)
        return domain_risks


    def finish(self):

        self.status = "CO"
        self.next_to_reply = "FI"
        super().save()
        return self.status


    def sent_notification(self, custom_message=None):
        from krm.configuration.models import Configuration

        if self.next_to_reply == "FI":
            return

        # Calculamos a quien debemos avisar
        if self.next_to_reply == "WR":
            user = self.responsible
        elif self.next_to_reply == "WS":
            user = self.supervisor
        else:
            user = None

        configuration = Configuration.objects.first()
        translation.activate(
            user.notification_language)

        context = {
            "site_url": settings.SITE_URL,
            "app_name": configuration.app_name,
            "preheader": _("Plan de remediación pendiente"),
            "BRAND": settings.BRAND,
            "app_name": configuration.app_name,
            "user_email": user.email,
            "MAIN_EMAIL": configuration.main_email,
            "site_url": settings.SITE_URL,
            "recovery_url": settings.SITE_URL + reverse("auth:remember_password_form"),
            "custom_message": custom_message,
        }
        body_html = render_to_string(
            "emails/remediation_plan/remediation_plan_supervisor.html",
            context,
        )
        context = {
            "content": body_html,
            "preheader": _("Plan de remediación pendiente"),
            "BRAND": settings.BRAND,
            "app_name": configuration.app_name,
            "user_email": user.email,
            "MAIN_EMAIL": configuration.main_email,
            "site_url": settings.SITE_URL,
            "recovery_url": settings.SITE_URL + reverse("auth:remember_password_form"),
        }

        body_html = render_to_string("emails/base-inline.html", context)
        from_email = settings.EMAIL_FROM
        if settings.EMAIL_BCC:
            bcc = settings.EMAIL_BCC
        else:
            bcc = ""

        subject, from_email, to = (
            _("{} - Plan de remediación pendiente".format(configuration.app_name)),
            from_email,
            user.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        if configuration.enable_emails:
            msg.send(fail_silently=False)
