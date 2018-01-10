# -*- coding: utf-8 -*-
from django.urls import path

from api.views import ImportedArchiveView

urlpatterns = [
    path(
        route='projects/upload/',
        view=ImportedArchiveView.as_view(),
        name='project-imported-archive'
    )
]
