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
    ALLOWED_MIMETYPES = ('application/zip',)
    # valid file extensions to be indexed and registered
    VALID_IMPORT_EXT = ['.html']

    class Meta:
        prefix = 'ALEXANDRIA'
