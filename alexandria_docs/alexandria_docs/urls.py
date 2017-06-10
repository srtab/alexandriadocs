"""alexandria_docs URL Configuration
"""
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from core.views import HomepageView


urlpatterns = [
    url(
        regex=r'^$',
        view=HomepageView.as_view(),
        name="homepage"
    ),
    url(
        regex=r'^projects/',
        view=include('projects.urls', namespace='projects')
    ),
    url(
        regex=r'^search/',
        view=include('search.urls', namespace='search')
    ),
    url(
        regex=r'^admin/',
        view=admin.site.urls
    ),
    url(
        regex=r'^api/(?P<version>v1)/',
        view=include('api.urls', namespace='api')
    )
]


if settings.DEBUG:  # pragma: no cover
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # serve static generated documentation on debug mode
    urlpatterns += static(
        settings.PROJECTS_SERVE_URL,
        document_root=settings.PROJECTS_SERVE_ROOT)
