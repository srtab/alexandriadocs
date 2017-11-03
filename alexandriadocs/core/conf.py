import os

from django.conf import settings  # NOQA

from appconf import AppConf


class AlexandriaAppConf(AppConf):
    # number of elements by page
    PAGINATE_BY = 20
    # number of results returned to select2 autocomplete
    AUTOCOMPLETE_RESULTS = 10
    # number of elements to show on history uploads
    UPLOADS_HISTORY_LIMIT = 10
    # upload allowed mimetypes
    ALLOWED_MIMETYPES = ('application/x-gzip',)
    # path appended to url to serve docs
    SERVE_URL = "/docs/"
    # file system path to store static sites
    SERVE_ROOT = os.path.join(settings.DATA_DIR, 'staticsites')
    # valid file extensions to be indexed and registered
    VALID_IMPORT_EXT = ['.html']

    class Meta:
        prefix = 'ALEXANDRIA'
