"""
base app."""

# Django
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BusinessGroupAppConfig(AppConfig):
    """Booking app config."""

    name = 'krc.business_group'
    verbose_name = _('Grupos empresariales')
