from alexandriadocs.settings import *  # NOQA


DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
    },
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
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
