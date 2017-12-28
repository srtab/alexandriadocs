# -*- coding: utf-8 -*-
from django.urls import path

from accounts.ajax import UserAutocompleteView
from accounts.views import ProfileUpdateView

base_urlpatterns = [
    path(
        route='<slug:slug>/',
        view=ProfileUpdateView.as_view(),
        name='index'
    ),
]

ajax_urlpatterns = [
    path(
        route='search/user/',
        view=UserAutocompleteView.as_view(),
        name='user-search'
    ),
]

urlpatterns = base_urlpatterns + ajax_urlpatterns
