"""Development settings."""

import datetime
from .base import *  # NOQA
from .base import env

# Base
DEBUG = env.bool('KRM_DJANGO_DEBUG')
DEV = env.bool('KRM_DJANGO_DEV')
# Static  files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False

MEDIA_ROOT = '/krm-media'
MEDIA_URL = '/media/'

# Security
SECRET_KEY = env.str('KRM_DJANGO_SECRET_KEY')

# Databases
DATABASES['default'] = env.db('DATABASE_URL')  # NOQA
DATABASES['default']['ATOMIC_REQUESTS'] = True  # NOQA
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)  # NOQA

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

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

# Gunicorn
INSTALLED_APPS += ['gunicorn']  # noqa F405

# WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa F405

# Email
# EMAIL_BACKEND = env.str('DJANGO_EMAIL_BACKEND')
# FROM_EMAIL = env.str('FROM_EMAIL')
# EMAIL_DEV_TO = env.str('EMAIL_DEV_TO')
# EMAIL_HOST = env.str('EMAIL_HOST')
# EMAIL_PORT = env.int('EMAIL_PORT')
# EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
# EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

INTERNAL_IPS = ('*',)


# WSGI
WSGI_APPLICATION = 'config.wsgi-production.application'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt': "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '/krm-logs/debug.log',
#             'maxBytes': 15728640,  # 1024 * 1024 * 15B = 15MB
#             'backupCount': 10,
#             'formatter': 'verbose',
#         },
#         'file_krm': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '/krm-logs/krm.log',
#             'maxBytes': 15728640,  # 1024 * 1024 * 15B = 15MB
#             'backupCount': 10,
#             'formatter': 'verbose',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'propagate': True,
#             'level': 'DEBUG',
#         },
#         'django.security.DisallowedHost': {
#             'level': 'ERROR',
#             'handlers': ['file_krm', 'mail_admins'],
#             'propagate': True
#         },
#         'krm': {
#             'handlers': ['file_krm'],
#             'level': 'DEBUG',
#         },
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True
#         },
#     }
# }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["file"]},
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "/krm-logs/django.log",
            "formatter": "app",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },
    },
    "formatters": {
        "app": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}

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
