# -*- coding: utf-8 -*-
from accounts.ajax import UserAutocompleteView
from accounts.views import ProfileUpdateView
from django.conf.urls import url


base_urlpatterns = [
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view=ProfileUpdateView.as_view(),
        name='index'
    ),
]

ajax_urlpatterns = [
    url(
        regex=r'^search/user/$',
        view=UserAutocompleteView.as_view(),
        name='user-search'
    ),
]

urlpatterns = base_urlpatterns + ajax_urlpatterns
