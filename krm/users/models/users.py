import math
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

import hashlib
from random import choice


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

    remember_key = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        verbose_name=_("Clave de recuperación de contraseña"),
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

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

        self.update_remember_key()
        remember_url = settings.SITE_URL + reverse(
            "auth:type_your_password", kwargs={"remember_key": self.remember_key}
        )

        context = {"remember_url": remember_url}
        body_html = render_to_string(
            "emails/users/welcome_email.html", context)
        context = {"content": body_html,
                   "preheader": _("Establecer contraseña")}
        body_html = render_to_string("emails/base-inline.html", context)
        from_email = settings.EMAIL_FROM
        if settings.EMAIL_BCC:
            bcc = settings.EMAIL_BCC
        else:
            bcc = ""

        subject, from_email, to = (
            _("KRM Tool - Nueva cuenta de usuario"),
            from_email,
            self.email,
        )
        msg = EmailMultiAlternatives(
            subject, body_html, from_email, [to], [bcc])
        msg.content_subtype = "html"

        self.add_action(_("Welcome email"))
        return msg.send(fail_silently=False)
