"""alexandriadocs URL Configuration
"""
from __future__ import unicode_literals

from django.conf.urls import url
from django.conf import settings

from projects.views import ProjectServeSiteView


urlpatterns = [
    url(
        regex=r'^(?P<path>.*)$',
        view=ProjectServeSiteView.as_view(),
        name="serve_docs"
    ),
]


if settings.DEBUG:  # pragma: no cover
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
