from django.conf import settings  # NOQA

from appconf import AppConf


class AlexandriaAppConf(AppConf):
    # number of elements by page
    PAGINATE_BY = 20
    # number of results returned to select2 autocomplete
    AUTOCOMPLETE_RESULTS = 10

    class Meta:
        prefix = 'ALEXANDRIA'
