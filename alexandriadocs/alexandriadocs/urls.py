"""alexandriadocs URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

from core.sitemaps import sitemaps
from core.views import HomepageView
from projects.views import ProjectServeDocs

# https://django-allauth.readthedocs.io/en/latest/advanced.html#admin
admin.site.login = login_required(admin.site.login)


urlpatterns = [
    path(
        route='',
        view=HomepageView.as_view(),
        name="homepage"
    ),
    path(
        route='docs/<slug:slug>/<path:path>',
        view=ProjectServeDocs.as_view(),
        name="serve-docs"
    ),
    path(
        route='accounts/',
        view=include('allauth.urls')
    ),
    path(
        route='accounts/',
        view=include(('accounts.urls', 'accounts'), namespace='accounts')
    ),
    path(
        route='groups/',
        view=include(('groups.urls', 'groups'), namespace='groups')
    ),
    path(
        route='projects/',
        view=include(('projects.urls', 'projects'), namespace='projects')
    ),
    path(
        route='search/',
        view=include(('search.urls', 'search'), namespace='search')
    ),
    path(
        route='admin/',
        view=admin.site.urls
    ),
    re_path(
        route=r'^api/(?P<version>v1)/',
        view=include(('api.urls', 'api'), namespace='api')
    ),
    path(
        route='sitemap.xml',
        view=sitemap,
        kwargs={'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    )
]


if settings.DEBUG:  # pragma: no cover
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += [
        path(
            route='__debug__/',
            view=include(debug_toolbar.urls)
        ),
    ]
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
