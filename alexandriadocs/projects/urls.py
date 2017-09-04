# -*- coding: utf-8 -*-
from django.conf.urls import url
from projects.views import (
    ProjectBadgeView, ProjectCreateView, ProjectDetailView, ProjectListView)


urlpatterns = [
    url(
        regex=r'^$',
        view=ProjectListView.as_view(),
        name='project-list'
    ),
    url(
        regex=r'^new/$',
        view=ProjectCreateView.as_view(),
        name='project-create'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view=ProjectDetailView.as_view(),
        name='project-detail'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/badge/$',
        view=ProjectBadgeView.as_view(),
        name='project-badge'
    ),
]
