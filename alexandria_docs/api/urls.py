from __future__ import unicode_literals

from django.conf.urls import url

from api.views import ImportArchiveView


urlpatterns = [
    url(
        regex=r'^projects/upload/$',
        view=ImportArchiveView.as_view(),
        name='project-import-archive'
    )
]
