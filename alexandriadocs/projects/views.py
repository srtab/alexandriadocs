# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from projects.models import Group, Project


BADGE_URL = (
    'https://img.shields.io/badge/docs-{status}-{color}.svg?style={style}'
)


@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    """ """
    model = Project


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(CreateView):
    """ """
    model = Project
    fields = ('title', 'description', 'group', 'repo', 'tags')
    success_url = reverse_lazy('projects:project-list')


@method_decorator(login_required, name='dispatch')
class GroupListView(ListView):
    """ """
    model = Group


@method_decorator(login_required, name='dispatch')
class GroupCreateView(CreateView):
    """ """
    model = Group
    fields = ('name',)
    success_url = reverse_lazy('projects:group-list')


class ProjectBadgeView(View):
    """ """

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
