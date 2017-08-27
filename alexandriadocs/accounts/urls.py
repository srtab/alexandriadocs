# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import ProfileUpdateView


urlpatterns = [
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=ProfileUpdateView.as_view(),
        name='index'
    ),
]
