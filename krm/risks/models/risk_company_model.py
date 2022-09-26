from tkinter import CASCADE
from django.db import models

from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from krm.utils.models import AuditModel


class RiskCompany(AuditModel):
    """Risk Company model.
    Modelo para representar  for represent a Risk Master
    """

    company = models.ForeignKey(
        'companies.Company',
        verbose_name=_('Compañía'),
        on_delete=models.CASCADE,
        related_name='krm_risks'
    )

    risk = models.ForeignKey(
        'risks.Risk',
        verbose_name=_("Riesgo original"),
        on_delete=models.CASCADE,
        related_name='risks_company'
    )

    name = models.CharField(
        verbose_name=_("Nombre"),
        max_length=140
    )

    description = RichTextField(
        _("Descripción"),
        config_name='awesome_ckeditor',
        max_length=10000
    )

    active = models.BooleanField(
        _('Activo'),
        default=False
    )

    krm_activity_affected = RichTextField(
        _("Actividad afectada"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True
    )

    krm_main_events = RichTextField(
        _("Describa los principales eventos en los que el riesgo se materializa o se espera que se materialice. Comentarios"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True
    )

    krm_exposed_staff = RichTextField(
        _("Personal especialmente expuesto al Riesgo"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True
    )

    krm_main_elements = RichTextField(
        _("Principales elementos del Riesgo"),
        config_name='awesome_ckeditor',
        max_length=10000,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Riesgo-Compañía")
        verbose_name_plural = _("Riesgos-Compañías")
        ordering = ["risk", "company"]
