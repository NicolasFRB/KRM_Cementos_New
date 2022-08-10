"""Development settings."""

import datetime
from .base import *  # NOQA
from .base import env

# Base
DEBUG = env.bool('DJANGO_DEBUG')
DEV = env.bool('DJANGO_DEV')
# Static  files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = '/krm-media'
MEDIA_URL = '/media/'

# Security
SECRET_KEY = env.str('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['*']

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

# Gunicorn
INSTALLED_APPS += ['gunicorn']  # noqa F405

# WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa F405

# Email
EMAIL_BACKEND = env.str('DJANGO_EMAIL_BACKEND')
FROM_EMAIL = env.str('FROM_EMAIL')
EMAIL_DEV_TO = env.str('EMAIL_DEV_TO')
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

INTERNAL_IPS = ('*',)


# WSGI
# WSGI_APPLICATION = 'config.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/krm-logs/debug.log',
            'maxBytes': 15728640,  # 1024 * 1024 * 15B = 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'file_krm': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/krm-logs/krm.log',
            'maxBytes': 15728640,  # 1024 * 1024 * 15B = 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['file_krm', 'mail_admins'],
            'propagate': True
        },
        'krm': {
            'handlers': ['file_krm'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
    }
}
