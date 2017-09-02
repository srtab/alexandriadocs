# -*- coding: utf-8 -*-
from django.conf.urls import url
from projects.views import ProjectBadgeView, ProjectCreateView, ProjectListView


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
        regex=r'^(?P<project_slug>[-\w]+)/badge/$',
        view=ProjectBadgeView.as_view(),
        name='project-badge'
    ),
]
