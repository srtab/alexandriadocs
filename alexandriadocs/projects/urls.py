# -*- coding: utf-8 -*-
from django.urls import path

from projects.ajax import (
    ImportedArchiveCreateView, ProjectCollaboratorCreateView,
    ProjectCollaboratorDeleteView, ProjectDeleteView,
    ProjectVisibilityUpdateView
)
from projects.views import (
    ProjectBadgeUrlView, ProjectBadgeView, ProjectCollaboratorsView,
    ProjectCreateView, ProjectDetailView, ProjectListView, ProjectSettingsView,
    ProjectUploadsView
)

base_urlpatterns = [
    path(
        route='',
        view=ProjectListView.as_view(),
        name='project-list'
    ),
    path(
        route='new/',
        view=ProjectCreateView.as_view(),
        name='project-create'
    ),
    path(
        route='<slug:slug>/',
        view=ProjectDetailView.as_view(),
        name='project-detail'
    ),
    path(
        route='<slug:slug>/badge/',
        view=ProjectBadgeView.as_view(),
        name='project-badge'
    ),
    path(
        route='<slug:slug>/uploads/',
        view=ProjectUploadsView.as_view(),
        name='project-uploads'
    ),
    path(
        route='<slug:slug>/collaborators/',
        view=ProjectCollaboratorsView.as_view(),
        name='project-collaborators'
    ),
    path(
        route='<slug:slug>/settings/',
        view=ProjectSettingsView.as_view(),
        name='project-settings'
    ),
    path(
        route='<slug:slug>/badge-url/',
        view=ProjectBadgeUrlView.as_view(),
        name='project-badge-url'
    )
]

ajax_urlpatterns = [
    path(
        route='<slug:project_slug>/uploads/new/',
        view=ImportedArchiveCreateView.as_view(),
        name='imported-archive-create'
    ),
    path(
        route='<slug:project_slug>/collaborators/new/',
        view=ProjectCollaboratorCreateView.as_view(),
        name='project-collaborator-create'
    ),
    path(
        route='<slug:project_slug>/collaborators/<int:pk>/delete/',
        view=ProjectCollaboratorDeleteView.as_view(),
        name='project-collaborator-delete'
    ),
    path(
        route='<slug:slug>/settings/visibility/',
        view=ProjectVisibilityUpdateView.as_view(),
        name='project-visibility-update'
    ),
    path(
        route='<slug:slug>/delete/',
        view=ProjectDeleteView.as_view(),
        name='project-delete'
    )
]

urlpatterns = base_urlpatterns + ajax_urlpatterns
