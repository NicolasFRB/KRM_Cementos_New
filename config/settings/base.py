import environ
from pathlib import Path
import os
from django.urls import reverse_lazy

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path("krm")

DEV = env.bool('KRM_DJANGO_DEV')
DEVJS = env.bool('KRM_DJANGO_DEVJS')
BRAND = env.str('KRM_BRAND')
KRM_DEBUG_TOOLBAR = env.bool('KRM_DEBUG_TOOLBAR', False)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9mgu=0t7adojsh2zgkfn2kw(a!@ob(t^3f6ebch3_q7(2=yn)v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("KRM_DJANGO_DEBUG")

ALLOWED_HOSTS = []

# Language and timezone
TIME_ZONE = "Europe/Madrid"
LANGUAGE_CODE = 'es'
USE_L10N = True
USE_I18N = True
USE_TZ = True

prefix_default_language = False


def gettext(s):
    return s


LANGUAGES = (
    ("en", gettext("English")),
    ("es", gettext("Spanish")),
)

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'whitenoise.runserver_nostatic',
]

THIRD_PARTY_APPS = [
    "crispy_forms",
    'django_extensions',
    'django_countries',
    'ckeditor',
    'django_filters',
    'rest_framework',
    'rosetta',
]

LOCAL_APPS = [
    'users',
    'configuration',
    'risks',
    'process',
    'controls',
    'companies',
    'evaluations',
    'evaluations_krm',
    'taskapp',
    'questionnaires',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
AUTH_USER_MODEL = 'users.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES
DATABASES = {
    "default": env.db("DATABASE_URL"),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, '_locale'),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(ROOT_DIR.path("krm").path('static')),
]

# Media
MEDIA_ROOT = "/krm-media"
MEDIA_URL = "/media/"

CRISPY_TEMPLATE_PACK = 'bootstrap4'

TEMPLATES_DIR = str(APPS_DIR.path("_templates"))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'krm.utils.context_processors.get_menu_urls',
            ],
            'libraries': {
                'theme': 'metronic.templatetags.theme',
            },
            'builtins': [
                'django.templatetags.static',
                'metronic.templatetags.theme',
            ]
        },
    },
]


# Email
EMAIL_BACKEND = env("KRM_DJANGO_EMAIL_BACKEND")
SERVER_EMAIL = "it@krctool.com"

# Admin
ADMIN_URL = "admin/"
ADMINS = [
    ("""Bienvenido Sáez Muelas""", "bienvenidosaez@baetica.com"),
]
MANAGERS = ADMINS

LOCALE_PATHS = (str(APPS_DIR.path("locale")),)

ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = "es"
ROSETTA_MESSAGES_SOURCE_LANGUAGE_NAME = "Spanish"
ROSETTA_MESSAGES_PER_PAGE = 100

LOGIN_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# URL config
SITE_URL = env.str("KRM_SITE_URL")

FILE_UPLOAD_PERMISSIONS = 0o640  # De audax
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = reverse_lazy('auth:login')


######################
# Keenthemes Settings
######################

# Theme Templates And "src" directories

KT_THEME_DIR = 'layout'


# Theme Mode
# Value: light | dark | system

KT_THEME_MODE_DEFAULT = 'light'
KT_THEME_MODE_SWITCH_ENABLED = True


# Theme Direction
# Value: ltr | rtl

KT_THEME_DIRECTION = 'ltr'


# Theme Assets

KT_THEME_ASSETS = {
    "favicon": "media/logos/favicon.ico",
    "fonts": [
        'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700',
    ],
    "css": [
        "plugins/global/plugins.bundle.css",
        "css/style.bundle.css"
    ],
    "js": [
        "plugins/global/plugins.bundle.js",
        "js/scripts.bundle.js"
    ]
}


# Theme Vendors

KT_THEME_VENDORS = {
    "datatables": {
        "css": [
            "plugins/custom/datatables/datatables.bundle.css"
        ],
        "js": [
            "plugins/custom/datatables/datatables.bundle.js"
        ]
    },
    "formrepeater": {
        "js": [
            "plugins/custom/formrepeater/formrepeater.bundle.js"
        ]
    },
    "fullcalendar": {
        "css": [
            "plugins/custom/fullcalendar/fullcalendar.bundle.css"
        ],
        "js": [
            "plugins/custom/fullcalendar/fullcalendar.bundle.js"
        ]
    },
    "flotcharts": {
        "js": [
            "plugins/custom/flotcharts/flotcharts.bundle.js"
        ]
    },
    "google-jsapi": {
        "js": [
            "//www.google.com/jsapi"
        ]
    },
    "tinymce": {
        "js": [
            "plugins/custom/tinymce/tinymce.bundle.js"
        ]
    },
    "ckeditor-custom": {
        "js": [
            "js/custom/custom-ckeditor/ckeditor.js",
        ]
    },
    "ckeditor-classic": {
        "js": [
            "plugins/custom/ckeditor/ckeditor-classic.bundle.js",
        ]
    },
    "ckeditor-inline": {
        "js": [
            "plugins/custom/ckeditor/ckeditor-inline.bundle.js"
        ]
    },
    "ckeditor-balloon": {
        "js": [
            "plugins/custom/ckeditor/ckeditor-balloon.bundle.js"
        ]
    },
    "ckeditor-balloon-block": {
        "js": [
            "plugins/custom/ckeditor/ckeditor-balloon-block.bundle.js"
        ]
    },
    "ckeditor-document": {
        "js": [
            "plugins/custom/ckeditor/ckeditor-document.bundle.js"
        ]
    },
    "draggable": {
        "js": [
            "plugins/custom/draggable/draggable.bundle.js"
        ]
    },
    "fslightbox": {
        "js": [
            "plugins/custom/fslightbox/fslightbox.bundle.js"
        ]
    },
    "jkanban": {
        "css": [
            "plugins/custom/jkanban/jkanban.bundle.css"
        ],
        "js": [
            "plugins/custom/jkanban/jkanban.bundle.js"
        ]
    },
    "typedjs": {
        "js": [
            "plugins/custom/typedjs/typedjs.bundle.js"
        ]
    },
    "cookiealert": {
        "css": [
            "plugins/custom/cookiealert/cookiealert.bundle.css"
        ],
        "js": [
            "plugins/custom/cookiealert/cookiealert.bundle.js"
        ]
    },
    "cropper": {
        "css": [
            "plugins/custom/cropper/cropper.bundle.css"
        ],
        "js": [
            "plugins/custom/cropper/cropper.bundle.js"
        ]
    },
    "vis-timeline": {
        "css": [
            "plugins/custom/vis-timeline/vis-timeline.bundle.css"
        ],
        "js": [
            "plugins/custom/vis-timeline/vis-timeline.bundle.js"
        ]
    },
    "jstree": {
        "css": [
            "plugins/custom/jstree/jstree.bundle.css"
        ],
        "js": [
            "plugins/custom/jstree/jstree.bundle.js"
        ]
    },
    "prismjs": {
        "css": [
            "plugins/custom/prismjs/prismjs.bundle.css"
        ],
        "js": [
            "plugins/custom/prismjs/prismjs.bundle.js"
        ]
    },
    "leaflet": {
        "css": [
            "plugins/custom/leaflet/leaflet.bundle.css"
        ],
        "js": [
            "plugins/custom/leaflet/leaflet.bundle.js"
        ]
    },
    "amcharts": {
        "js": [
            "https://cdn.amcharts.com/lib/5/index.js",
            "https://cdn.amcharts.com/lib/5/xy.js",
            "https://cdn.amcharts.com/lib/5/percent.js",
            "https://cdn.amcharts.com/lib/5/radar.js",
            "https://cdn.amcharts.com/lib/5/themes/Animated.js"
        ]
    },
    "amcharts-maps": {
        "js": [
            "https://cdn.amcharts.com/lib/5/index.js",
            "https://cdn.amcharts.com/lib/5/map.js",
            "https://cdn.amcharts.com/lib/5/geodata/worldLow.js",
            "https://cdn.amcharts.com/lib/5/geodata/continentsLow.js",
            "https://cdn.amcharts.com/lib/5/geodata/usaLow.js",
            "https://cdn.amcharts.com/lib/5/geodata/worldTimeZonesLow.js",
            "https://cdn.amcharts.com/lib/5/geodata/worldTimeZoneAreasLow.js",
            "https://cdn.amcharts.com/lib/5/themes/Animated.js"
        ]
    },
    "amcharts-stock": {
        "js": [
            "https://cdn.amcharts.com/lib/5/index.js",
            "https://cdn.amcharts.com/lib/5/xy.js",
            "https://cdn.amcharts.com/lib/5/themes/Animated.js"
        ]
    },
    "bootstrap-select": {
        "css": [
            "plugins/custom/bootstrap-select/bootstrap-select.bundle.css"
        ],
        "js": [
            "plugins/custom/bootstrap-select/bootstrap-select.bundle.js"
        ]
    }
}


CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format', ],
            ['Bold',
             'Italic',
             'Link',
             'Unlink',
             'NulletedList',
             'NumberedList',
             'RemoveFormat', ],
            ['Undo',
             'Redo',
             'Source']
        ]
    },
}


# Email
EMAIL_BACKEND = env.str("KRM_DJANGO_EMAIL_BACKEND")
EMAIL_FROM = env.str("KRM_EMAIL_FROM")
EMAIL_HOST = env.str("KRM_EMAIL_HOST")
EMAIL_PORT = env.int("KRM_EMAIL_PORT")
EMAIL_USE_TLS = env.bool("KRM_EMAIL_USE_TLS")
EMAIL_HOST_USER = env.str("KRM_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("KRM_EMAIL_HOST_PASSWORD")
EMAIL_BCC = env.str("KRM_EMAIL_BCC")

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 99999,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:3000',
    'http://app.krmtool.com',
    'https://app.krmtool.com',
    'localhost:8000',
    'localhost:3000',
    'app.krmtool.com',
    'app.krmtool.com',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:3000',
    'http://app.krmtool.com',
    'https://app.krmtool.com',
    'localhost:8000',
    'localhost:3000',
    'app.krmtool.com',
    'app.krmtool.com',
]

ALLOWED_HOSTS = [
    'http://localhost:8000',
    'http://localhost:3000',
    'http://app.krmtool.com',
    'https://app.krmtool.com',
    'localhost:8000',
    'localhost:3000',
    'app.krmtool.com',
    'app.krmtool.com',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

KRM_ACTIVATE = env.bool("KRM_ACTIVATE")
