# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import SearchPageView, SearchProjectView


urlpatterns = [
    url(
        regex=r'^$',
        view=SearchProjectView.as_view(),
        name='index'
    ),
    url(
        regex=r'^pages/$',
        view=SearchPageView.as_view(),
        name='pages'
    ),
]
