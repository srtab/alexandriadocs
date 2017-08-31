# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import GroupListView, ProjectBadgeView, ProjectListView


urlpatterns = [
    url(
        regex=r'^$',
        view=ProjectListView.as_view(),
        name='index'
    ),
    url(
        regex=r'^groups/$',
        view=GroupListView.as_view(),
        name='group-list'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/badge/$',
        view=ProjectBadgeView.as_view(),
        name='project-badge'
    ),
]
