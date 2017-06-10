from __future__ import unicode_literals

from alexandria_docs.settings import *  # NOQA


DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
    },
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}


# LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        }
    },
    'loggers': {
        'alexandria': {
            'level': 'INFO',
            'handlers': ['null']
        }
    },
}
