from xmlrpc.client import DateTime
from django.utils import timezone
import requests

from django.db import models

from django.utils.translation import gettext_lazy as _

from krm.utils.models import SingletonModel
# Create your models here.


class Configuration(SingletonModel):
    app_name = models.CharField(
        verbose_name='Nombre de la aplicación',
        max_length=140
    )
    main_email = models.EmailField(
        verbose_name='Email principal',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.app_name

    class Meta:
        verbose_name = _("Configuración")
        verbose_name_plural = _("Configuración")
        ordering = ["app_name"]
