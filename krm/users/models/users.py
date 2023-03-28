import math
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import translation

import hashlib
from random import choice

from krm.configuration.models import Configuration


def random_digits(number_digits=6):
    import random
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(number_digits):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    return random_str


def md5_generate(n=20, en_md5=True):
    valores = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+'
    p = ''
    p = p.join([choice(valores) for i in range(n)])
    if en_md5:
        p = hashlib.md5(p.encode()).hexdigest()
    return p


class User(AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    companies = models.ManyToManyField(
        'companies.Company',
        related_name="employees",
        verbose_name=_("Compañías a las que pertenece"),
        blank=True,
    )

    companies_admin = models.ManyToManyField(
        'companies.Company',
        related_name="admins",
        verbose_name=_("Compañías qué administra"),
        blank=True,
    )

    remember_key = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        verbose_name=_("Clave de recuperación de contraseña"),
    )

    position = models.CharField(
        blank=True,
        null=True,
        max_length=140,
        verbose_name=_("Cargo que ocupa"),
    )

    NOTIFICATION_LANT_CHOICES = (
        ('es', _('Español')),
        ('en', _('English')),
    )

    notification_language = models.CharField(
        max_length=2,
        choices=NOTIFICATION_LANT_CHOICES,
        default='es',
        verbose_name=_("Idioma de notificaciones"),
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def username_no_domain(self):
        return '%s' % self.email.split('@')[0]

    @property
    def is_company_admin(self):
        return self.companies_admin.count() > 0

    @property
    def is_admin(self):
        return self.is_company_admin or self.is_superuser

    def controls_test_supervisor_pending(self):
        return self.controls_test_supervisor.filter(status="WS")

    def controls_test_owner_pending(self):
        return self.controls_test_owner.filter(status="WO")

    def controls_test_administrator_pending(self):
        from krm.evaluations.models import ControlTest
        return ControlTest.objects.filter(status="WA", evaluation__company__in=self.companies_admin.all())

    def controls_test_administrator_finished(self):
        from krm.evaluations.models import ControlTest
        return ControlTest.objects.filter(status="FI", evaluation__company__in=self.companies_admin.all())

    # Risk Test Inherent

    def evaluation_krm_inherent_pending(self):
        from krm.evaluations_krm.models import EvaluationKrmInherent
        return EvaluationKrmInherent.objects.filter(
            risk_test_inherents__status=1,
            risk_test_inherents__expert=self,
        ).distinct()

    def evaluation_krm_inherent_delivered(self):
        from krm.evaluations_krm.models import EvaluationKrmInherent
        return EvaluationKrmInherent.objects.filter(
            risk_test_inherents__status=2,
            risk_test_inherents__expert=self,
        ).distinct()

    def evaluation_krm_inherent_finished(self):
        from krm.evaluations_krm.models import EvaluationKrmInherent
        return EvaluationKrmInherent.objects.filter(
            risk_test_inherents__status=3,
            risk_test_inherents__expert=self,
        ).distinct()

    def risk_test_inherent_expert_pending(self):
        return self.risk_test_inherents.filter(status=1)

    # Risk Test Residual

    def evaluation_krm_residual_pending(self):
        from krm.evaluations_krm.models import EvaluationKrmResidual
        return EvaluationKrmResidual.objects.filter(
            risk_test_residuals__status=1,
            risk_test_residuals__evaluator=self,
        ).distinct()

    def evaluation_krm_residual_delivered(self):
        from krm.evaluations_krm.models import EvaluationKrmResidual
        return EvaluationKrmResidual.objects.filter(
            risk_test_residuals__status=2,
            risk_test_residuals__evaluator=self,
        ).distinct()

    def evaluation_krm_residual_finished(self):
        from krm.evaluations_krm.models import EvaluationKrmResidual
        return EvaluationKrmResidual.objects.filter(
            risk_test_residuals__status=3,
            risk_test_residuals__evaluator=self,
        ).distinct()

    def risk_test_residual_evaluator_pending(self):
        return self.risk_test_residuals.filter(status=1)

    # Questionnaires
    def evaluation_questionnaires_pending(self):
        from krm.questionnaires.models import EvaluationQuestionnaire
        return EvaluationQuestionnaire.objects.filter(
            question_tests__status=1,
            question_tests__evaluator=self,
        ).distinct()

    def question_test_pending(self):
        from krm.questionnaires.models import QuestionTest
        return QuestionTest.objects.filter(
            status=1,
            evaluator=self,
        )
    
    def total_pending_actions(self):
        return self.controls_test_owner_pending().count() + self.controls_test_supervisor_pending().count() + self.risk_test_inherent_expert_pending().count() + self.risk_test_residual_evaluator_pending().count() + self.question_test_pending().count()

    def save(self, *args, **kwargs):
        self.username = self.email
        if not self.remember_key:
            self.remember_key = md5_generate()
        super(User, self).save(*args, **kwargs)

    def add_action(self, action_description):
        from krm.users.models import ActionLogUser
        ActionLogUser.objects.create(
            user=self, action_description=action_description
        )

    def update_remember_key(self):
        self.remember_key = md5_generate()
        self.save()

    def send_welcome_email(self):
        from django.conf import settings
        from krm.configuration.models import Configuration

        configuration = Configuration.objects.first()

        translation.activate(self.notification_language)

        self.update_remember_key()
        remember_url = settings.SITE_URL + reverse(
            "auth:type_your_password", kwargs={"remember_key": self.remember_key}
        )

        context = {
            "remember_url": remember_url,
            "app_name": configuration.app_name,
        }
        body_html = render_to_string(
            "emails/users/welcome_email.html", context)
        context = {
            "content": body_html,
            "preheader": _("Establecer contraseña"),
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
            _("{} - Nueva cuenta de usuario".format(configuration.app_name)),
            from_email,
            self.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.add_action(_("Welcome email"))

        if configuration.enable_emails:
            return msg.send(fail_silently=False)
        else:
            return True

    def send_email_remember_password(self):
        from krm.configuration.models import Configuration

        configuration = Configuration.objects.first()

        translation.activate(self.notification_language)

        self.update_remember_key()
        remember_url = settings.SITE_URL + reverse(
            "auth:type_your_password", kwargs={"remember_key": self.remember_key}
        )

        context = {
            "remember_url": remember_url,
            "app_name": configuration.app_name,
        }
        body_html = render_to_string(
            "emails/users/remember_password.html", context)
        context = {
            "content": body_html,
            "preheader": _("Recordar contraseña"),
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
            _("{} - Cambio de contraseña".format(configuration.app_name)),
            from_email,
            self.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.add_action(_("Reset password email"))

        if configuration.enable_emails:
            msg.send(fail_silently=False)
