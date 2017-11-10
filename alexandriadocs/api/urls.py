# -*- coding: utf-8 -*-
from django.conf.urls import url

from api.views import ImportedArchiveView

urlpatterns = [
    url(
        regex=r'^projects/upload/$',
        view=ImportedArchiveView.as_view(),
        name='project-imported-archive'
    )
]
