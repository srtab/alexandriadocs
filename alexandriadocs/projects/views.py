# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.views.generic import View
from django.views.static import serve
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings

from projects.models import Project


BADGE_URL = (
    'https://img.shields.io/badge/docs-{status}-{color}.svg?style={style}'
)


class ProjectBadgeView(View):

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('project_slug')
        style = self.kwargs.get('style', 'flat-square')
        project = Project.objects.filter(slug=slug).first()
        if not project:
            url = BADGE_URL.format(
                status="unknown", color='lightgrey', style=style)
            return redirect(url)
        url = BADGE_URL.format(
            status="latest", color='brightgreen', style=style)
        return redirect(url)


class ProjectServeSiteView(View):

    def get(self, request, *args, **kwargs):
        get_object_or_404(Project, slug=request.slug)
        filename = "{slug}/{filename}".format(
            slug=request.slug,
            filename=self.kwargs.get('path') or "index.html")
        serve_root = settings.PROJECTS_SERVE_ROOT
        if settings.DEBUG:
            # Serve with Python
            return serve(request, filename, serve_root)
        else:
            pass
            # TODO
