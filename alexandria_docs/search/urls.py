# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from .views import SearchProjectView, SearchPageView


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
