"""alexandriadocs URL Configuration
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from core.views import HomepageView
from projects.views import ProjectServeDocs

# https://django-allauth.readthedocs.io/en/latest/advanced.html#admin
admin.site.login = login_required(admin.site.login)


urlpatterns = [
    url(
        regex=r'^$',
        view=HomepageView.as_view(),
        name="homepage"
    ),
    url(
        regex=r'^docs/(?P<slug>[-\w]+)/(?P<path>.*)$',
        view=ProjectServeDocs.as_view(),
        name="serve-docs"
    ),
    url(
        regex=r'^accounts/',
        view=include('allauth.urls')
    ),
    url(
        regex=r'^accounts/',
        view=include('accounts.urls', namespace='accounts')
    ),
    url(
        regex=r'^groups/',
        view=include('groups.urls', namespace='groups')
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
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
