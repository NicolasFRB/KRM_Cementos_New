"""Development settings."""

import datetime
from .base import *  # NOQA
from .base import env
import os

# Base
DEBUG = env.bool('KRM_DJANGO_DEBUG')
DEV = env.bool('KRM_DJANGO_DEV')

# Security
SECRET_KEY = env.str('KRM_DJANGO_SECRET_KEY')
ALLOWED_HOSTS = [
    "*"
]

INTERNAL_IPS = (
    "*"
)

CORS_ORIGIN_WHITELIST = [
    "*",
]

CSRF_TRUSTED_ORIGINS = [
    'https://4924-81-38-122-210.eu.ngrok.io/'
    '*',
]


# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

if DEV:
    INSTALLED_APPS += ['debug_toolbar']  # noqa F405
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
