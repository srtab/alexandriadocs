from __future__ import unicode_literals

from django.conf.urls import url

from api.views import UploadProjectArchiveView


urlpatterns = [
    url(
        regex=r'^projects/upload/$',
        view=UploadProjectArchiveView.as_view(),
        name='project-archive-upload'
    )
]
