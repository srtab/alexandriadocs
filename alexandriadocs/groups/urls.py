# -*- coding: utf-8 -*-
from django.conf.urls import url

from groups.ajax import (
    GroupAutocompleteView, GroupCollaboratorCreateView,
    GroupCollaboratorDeleteView, GroupVisibilityUpdateView,
    GroupDeleteView
)
from groups.views import (
    GroupCollaboratorsView, GroupCreateView, GroupDetailView,
    GroupListView, GroupSettingsView
)

base_urlpatterns = [
    url(
        regex=r'^$',
        view=GroupListView.as_view(),
        name='group-list'
    ),
    url(
        regex=r'^new/$',
        view=GroupCreateView.as_view(),
        name='group-create'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view=GroupDetailView.as_view(),
        name='group-detail'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/collaborators/$',
        view=GroupCollaboratorsView.as_view(),
        name='group-collaborators'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/settings/$',
        view=GroupSettingsView.as_view(),
        name='group-settings'
    )
]

ajax_urlpatterns = [
    url(
        regex=r'^search/group/$',
        view=GroupAutocompleteView.as_view(),
        name='group-search'
    ),
    url(
        regex=r'^(?P<group_slug>[-\w]+)/collaborators/new/$',
        view=GroupCollaboratorCreateView.as_view(),
        name='group-collaborator-create'
    ),
    url(
        regex=r'^(?P<group_slug>[-\w]+)/collaborators/(?P<pk>\d+)/delete/$',
        view=GroupCollaboratorDeleteView.as_view(),
        name='group-collaborator-delete'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/settings/visibility/$',
        view=GroupVisibilityUpdateView.as_view(),
        name='group-visibility-update'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/settings/delete/$',
        view=GroupDeleteView.as_view(),
        name='group-delete'
    )
]


urlpatterns = base_urlpatterns + ajax_urlpatterns
