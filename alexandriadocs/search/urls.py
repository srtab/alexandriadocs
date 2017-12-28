# -*- coding: utf-8 -*-
from django.urls import path

from search.views import SearchPageView, SearchProjectView

urlpatterns = [
    path(
        route='',
        view=SearchProjectView.as_view(),
        name='index'
    ),
    path(
        route='pages/',
        view=SearchPageView.as_view(),
        name='pages'
    ),
]
