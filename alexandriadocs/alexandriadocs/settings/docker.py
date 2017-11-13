import mimetypes

from alexandriadocs.settings import *  # NOQA

# to serve svg images on development mode
mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alexandria',
        'USER': 'postgres',
        'PASSWORD': 'dbrootpass',
        'HOST': 'db'
    }
}


# DEBUG TOOLBAR
INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda x: True
}


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',  # noqa
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'alexandria',
    },
}


SENDFILE_BACKEND = "sendfile.backends.development"


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
