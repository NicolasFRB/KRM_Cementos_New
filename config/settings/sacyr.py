"""Development settings."""

import datetime
from .base import *  # NOQA
from .base import env
import os

# Base
DEBUG = env.bool('KRM_DJANGO_DEBUG')

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
    'http://localhost:8000',
    'http://localhost:3000',
    'http://app.krmtool.com',
    'https://app.krmtool.com',
    'http://krmtool.sacyr.com',
    'https://krctool.sacyr.com'
]


# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

if KRM_DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    import socket  # only if you haven't already imported this
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [
        ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


# Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_TASK_TIME_LIMIT = 5 * 60
CELERYD_TASK_SOFT_TIME_LIMIT = 60
CELERY_TIMEZONE = 'Europe/Madrid'
CELERY_TASK_DEFAULT_QUEUE = "krm"
CELERY_TASK_DEFAULT_EXCHANGE = "krm"
CELERY_TASK_DEFAULT_ROUTING_KEY = "krm"


# # WhiteNoise
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa F405

# # Static  files
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# WHITENOISE_MANIFEST_STRICT = False
# INSTALLED_APPS += ['whitenoise.runserver_nostatic']  # noqa F405
