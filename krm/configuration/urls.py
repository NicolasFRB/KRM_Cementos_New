"""Main URLs module."""

from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from .views import (
    ConfigurationUpdateView,
    ConfigurationDetailView
)

urlpatterns = [
    path("configuration/", ConfigurationDetailView.as_view(),
         name="configuration_detail"),
    path("configuration/update/",
         ConfigurationUpdateView.as_view(), name="configuration_update"),
]
