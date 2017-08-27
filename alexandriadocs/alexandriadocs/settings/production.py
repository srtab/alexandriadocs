from __future__ import unicode_literals

import os

from alexandriadocs.settings import *  # NOQA


DEBUG = False
COMPRESS_OFFLINE = True


ALLOWED_HOSTS = [os.environ.get('DJ_ALLOWED_HOSTS')]
SECRET_KEY = os.environ.get('DJ_SECRET_KEY')


# database configs

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    }
}


# elasticsearch configs

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',  # noqa
        'URL': os.environ.get('ES_URL'),
        'INDEX_NAME': os.environ.get('ES_INDEX'),
    },
}


# Caching

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_LOCATION'),
        "KEY_PREFIX": "alexandria",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Google analytics tracking ID

ANALYTICS_TRACKING_ID = os.environ.get('ANALYTICS_TRACKING_ID')


# Sentry configurations

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
    'release': 'v0.1.0-alpha.1',
    'environment': 'production'
}


# EMAIL configs

DEFAULT_FROM_EMAIL = 'no-reply@alexandriadocs.io'
EMAIL_HOST = os.environ.get('SMTP_HOST')
EMAIL_PORT = os.environ.get('SMTP_PORT')
EMAIL_HOST_USER = os.environ.get('SMTP_USER')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASS')
EMAIL_USE_TLS = True


# SSL

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
