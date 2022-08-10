from .dev import *  # NOQA

TEST_RUNNER = "django.test.runner.DiscoverRunner"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
