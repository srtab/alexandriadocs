# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import ProjectBadgeView


urlpatterns = [
    url(
        regex=r'^(?P<project_slug>[-\w]+)/badge/$',
        view=ProjectBadgeView.as_view(),
        name='badge'
    ),
]
