from __future__ import unicode_literals

import mimetypes

from alexandria_docs.settings import *  # NOQA


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
