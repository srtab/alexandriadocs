# -*- coding: utf-8 -*-
from django.urls import path

from groups.ajax import (
    GroupAutocompleteView, GroupCollaboratorCreateView,
    GroupCollaboratorDeleteView, GroupDeleteView, GroupVisibilityUpdateView
)
from groups.views import (
    GroupCollaboratorsView, GroupCreateView, GroupDetailView, GroupListView,
    GroupSettingsView
)

base_urlpatterns = [
    path(
        route='',
        view=GroupListView.as_view(),
        name='group-list'
    ),
    path(
        route='new/',
        view=GroupCreateView.as_view(),
        name='group-create'
    ),
    path(
        route='<slug:slug>/',
        view=GroupDetailView.as_view(),
        name='group-detail'
    ),
    path(
        route='<slug:slug>/collaborators/',
        view=GroupCollaboratorsView.as_view(),
        name='group-collaborators'
    ),
    path(
        route='<slug:slug>/settings/',
        view=GroupSettingsView.as_view(),
        name='group-settings'
    )
]

ajax_urlpatterns = [
    path(
        route='search/group/',
        view=GroupAutocompleteView.as_view(),
        name='group-search'
    ),
    path(
        route='<slug:group_slug>/collaborators/new/',
        view=GroupCollaboratorCreateView.as_view(),
        name='group-collaborator-create'
    ),
    path(
        route='<slug:group_slug>/collaborators/<int:pk>/delete/',
        view=GroupCollaboratorDeleteView.as_view(),
        name='group-collaborator-delete'
    ),
    path(
        route='<slug:slug>/settings/visibility/',
        view=GroupVisibilityUpdateView.as_view(),
        name='group-visibility-update'
    ),
    path(
        route='<slug:slug>/settings/delete/',
        view=GroupDeleteView.as_view(),
        name='group-delete'
    )
]


urlpatterns = base_urlpatterns + ajax_urlpatterns
