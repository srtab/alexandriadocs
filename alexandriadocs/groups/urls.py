# -*- coding: utf-8 -*-
from django.conf.urls import url

from groups.views import GroupCreateView, GroupListView


urlpatterns = [
    url(
        regex=r'^$',
        view=GroupListView.as_view(),
        name='group-list'
    ),
    url(
        regex=r'^new/$',
        view=GroupCreateView.as_view(),
        name='group-create'
    )
]
