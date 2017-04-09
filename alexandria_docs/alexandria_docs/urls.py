"""alexandria_docs URL Configuration
"""
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(
        regex=r'^admin/',
        view=admin.site.urls
    ),
    url(
        regex=r'^api-auth/',
        view=include('rest_framework.urls', namespace='rest_framework')
    ),
    url(
        regex=r'^api/(?P<version>v1)/',
        view=include('api.urls', namespace='api')
    )
]
