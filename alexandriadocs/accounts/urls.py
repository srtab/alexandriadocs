# -*- coding: utf-8 -*-
from accounts.views import ProfileUpdateView
from django.conf.urls import url


urlpatterns = [
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view=ProfileUpdateView.as_view(),
        name='index'
    ),
]
