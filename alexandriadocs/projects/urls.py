# -*- coding: utf-8 -*-
from django.conf.urls import url
from projects.views import (
    ProjectBadgeUrlView, ProjectBadgeView, ProjectCollaboratorsView,
    ProjectCreateView, ProjectDeleteView, ProjectDetailView, ProjectListView,
    ProjectSettingsView)


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
        regex=r'^(?P<slug>[-\w]+)/badge/$',
        view=ProjectBadgeView.as_view(),
        name='project-badge'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/collaborators/$',
        view=ProjectCollaboratorsView.as_view(),
        name='project-collaborators'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/settings/$',
        view=ProjectSettingsView.as_view(),
        name='project-settings'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/delete/$',
        view=ProjectDeleteView.as_view(),
        name='project-delete'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/badge-url/$',
        view=ProjectBadgeUrlView.as_view(),
        name='project-badge-url'
    ),
]
