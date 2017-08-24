from __future__ import unicode_literals

from api.views import ImportArchiveView
from django.conf.urls import url


urlpatterns = [
    url(
        regex=r'^projects/upload/$',
        view=ImportArchiveView.as_view(),
        name='project-import-archive'
    )
]
