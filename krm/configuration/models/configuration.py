from django.db import models

from django.utils.translation import gettext_lazy as _

from krm.utils.models import SingletonModel


class Configuration(SingletonModel):
    app_name = models.CharField(
        verbose_name='Nombre de la aplicación',
        max_length=140
    )
    main_email = models.CharField(
        verbose_name=_('Email principal'),
        blank=True,
        null=True,
        max_length=140
    )
    enable_emails = models.BooleanField(
        verbose_name=_('Habilitar envío de emails'),
        default=False
    )

    def __str__(self):
        return self.app_name

    class Meta:
        verbose_name = _("Configuración")
        verbose_name_plural = _("Configuración")
        ordering = ["app_name"]
