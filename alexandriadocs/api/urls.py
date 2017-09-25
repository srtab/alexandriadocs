# -*- coding: utf-8 -*-
from api.views import ImportedArchiveView
from django.conf.urls import url


urlpatterns = [
    url(
        regex=r'^projects/upload/$',
        view=ImportedArchiveView.as_view(),
        name='project-imported-archive'
    )
]
