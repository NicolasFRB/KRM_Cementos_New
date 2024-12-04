import environ
from pathlib import Path
import os
from django.urls import reverse_lazy

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path("krm")

DEV = True # env.bool('KRM_DJANGO_DEV')
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
    'health_check',                             # required
    # 'health_check.db',                          # stock Django health checkers

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
    # "cookiealert": {
    #     "css": [
    #         "plugins/custom/cookiealert/cookiealert.bundle.css"
    #     ],
    #     "js": [
    #         "plugins/custom/cookiealert/cookiealert.bundle.js"
    #     ]
    # },
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
    # "amcharts": {
    #     "js": [
    #         "https://cdn.amcharts.com/lib/5/index.js",
    #         "https://cdn.amcharts.com/lib/5/xy.js",
    #         "https://cdn.amcharts.com/lib/5/percent.js",
    #         "https://cdn.amcharts.com/lib/5/radar.js",
    #         "https://cdn.amcharts.com/lib/5/themes/Animated.js"
    #     ]
    # },
    # "amcharts-maps": {
    #     "js": [
    #         "https://cdn.amcharts.com/lib/5/index.js",
    #         "https://cdn.amcharts.com/lib/5/map.js",
    #         "https://cdn.amcharts.com/lib/5/geodata/worldLow.js",
    #         "https://cdn.amcharts.com/lib/5/geodata/continentsLow.js",
    #         "https://cdn.amcharts.com/lib/5/geodata/usaLow.js",
    #         "https://cdn.amcharts.com/lib/5/geodata/worldTimeZonesLow.js",
    #         "https://cdn.amcharts.com/lib/5/geodata/worldTimeZoneAreasLow.js",
    #         "https://cdn.amcharts.com/lib/5/themes/Animated.js"
    #     ]
    # },
    # "amcharts-stock": {
    #     "js": [
    #         "https://cdn.amcharts.com/lib/5/index.js",
    #         "https://cdn.amcharts.com/lib/5/xy.js",
    #         "https://cdn.amcharts.com/lib/5/themes/Animated.js"
    #     ]
    # },
    # "bootstrap-select": {
    #     "css": [
    #         "plugins/custom/bootstrap-select/bootstrap-select.bundle.css"
    #     ],
    #     "js": [
    #         "plugins/custom/bootstrap-select/bootstrap-select.bundle.js"
    #     ]
    # }
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
    'http://localhost:53660', # pruebas kubernetes
    'http://localhost:3000',
    'http://app.krmtool.com',
    'https://app.krmtool.com',
    'localhost:8000',
    'localhost:3000',
    'app.krmtool.com',
    'app.krmtool.com',
    'cstool.sacyr.com',
    'cstool.sacyr.com:444',
    'http://cstool.sacyr.com:444'
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:3000',
    'http://app.krmtool.com',
    'https://app.krmtool.com',
    'http://cstool.sacyr.com:444'
]

ALLOWED_HOSTS = [
    'http://localhost:8000',
    'http://localhost:53660', # pruebas kubernetes
    'http://localhost:3000',
    'http://app.krmtool.com',
    'https://app.krmtool.com',
    'localhost:8000',
    'localhost:3000',
    'app.krmtool.com',
    'app.krmtool.com',
    'cstool.sacyr.com',
    'cstool.sacyr.com:444',
    'http://cstool.sacyr.com:444'
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

KRM_ACTIVATE = env.bool("KRM_ACTIVATE")


# Load Auth0 application settings into memory
AUTH0_DOMAIN = env.str("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = env.str("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = env.str("AUTH0_CLIENT_SECRET")



# SAML2
SAML2_AUTH = {
    # Metadata is required, choose either remote url or local file path
    # 'METADATA_AUTO_CONF_URL': '[The auto(dynamic) metadata configuration URL of SAML2]',
    'METADATA_LOCAL_FILE_PATH': os.path.join( BASE_DIR, 'dev-metadata.xml'),

    # Optional settings below
    'DEFAULT_NEXT_URL': '/en/auth/callback/',  # Custom target redirect URL after the user get logged in. Default to /admin if not set. This setting will be overwritten if you have parameter ?next= specificed in the login URL.
    'CREATE_USER': False, # Create a new Django user when a new user logs in. Defaults to True.
    'NEW_USER_PROFILE': {
        'USER_GROUPS': [],  # The default group name when a new user logs in
        'ACTIVE_STATUS': True,  # The default active status for new users
        'STAFF_STATUS': True,  # The staff status for new users
        'SUPERUSER_STATUS': False,  # The superuser status for new users
    },
    'ATTRIBUTES_MAP': {  # Change Email/UserName/FirstName/LastName to corresponding SAML2 userprofile attributes.
        'email': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress',
        'username': 'http://schemas.auth0.com/nickname',
        'name': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name',
        # 'last_name': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname',
    },
    # 'TRIGGER': {
    #     'CREATE_USER': 'path.to.your.new.user.hook.method',
    #     'BEFORE_LOGIN': 'path.to.your.login.hook.method',
    # },
    'ASSERTION_URL': 'https://krm-tool-uat.des-onprem1.eci.geci', # Custom URL to validate incoming SAML requests against
    'ENTITY_ID': 'https://krm-tool-uat.des-onprem1.eci.geci/en/auth/callback/', # Populates the Issuer element in authn request
    'NAME_ID_FORMAT': None, # Sets the Format property of authn NameIDPolicy element
    'USE_JWT': False, # Set this to True if you are running a Single Page Application (SPA) with Django Rest Framework (DRF), and are using JWT authentication to authorize client users
    'FRONTEND_URL': 'https://krm-tool-uat.des-onprem1.eci.geci', # Redirect URL for the client if you are using JWT auth with DRF. See explanation below
    'XMLSEC_BINARY': '/usr/bin/xmlsec1',  # Ajusta esta ruta
 
}

HEALTH_CHECK = {
        # .....
        "SUBSETS": {
            "startup-probe": ["MigrationsHealthCheck", "KrmToolSimpleCheck"],
            "liveness-probe": ["KrmToolSimpleCheck"]        
        },
        # .....
    }