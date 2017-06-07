from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from .views import SearchView


urlpatterns = [
    url(
        regex=r'^$',
        view=SearchView.as_view(),
        name='index'
    ),
]
