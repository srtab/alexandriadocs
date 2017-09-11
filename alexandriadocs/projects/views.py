# -*- coding: utf-8 -*-
from core.views import SuccessDeleteMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from projects.forms import ProjectForm
from projects.models import Project


BADGE_URL = (
    'https://img.shields.io/badge/docs-{status}-{color}.svg?style={style}'
)


@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    """ """
    model = Project


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(SuccessMessageMixin, CreateView):
    """ """
    model = Project
    fields = ('title', 'description', 'group', 'repo', 'tags')
    success_url = reverse_lazy('projects:project-list')
    success_message = _("%(title)s was created successfully")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    """ """
    model = Project

    def get_queryset(self):
        return self.model._default_manager.visible(self.request.user)


@method_decorator(login_required, name='dispatch')
class ProjectBadgeView(DetailView):
    """ """
    model = Project
    template_name_suffix = '_badge'

    def get_queryset(self):
        return self.model._default_manager.author(self.request.user)


@method_decorator(login_required, name='dispatch')
class ProjectCollaboratorsView(DetailView):
    """ """
    model = Project
    template_name_suffix = '_collaborators'

    def get_queryset(self):
        return self.model._default_manager.author(self.request.user)


@method_decorator(login_required, name='dispatch')
class ProjectSettingsView(SuccessMessageMixin, UpdateView):
    """ """
    model = Project
    form_class = ProjectForm
    template_name_suffix = '_settings'
    success_message = _("%(title)s was updated successfully")

    def get_queryset(self):
        return self.model._default_manager.author(self.request.user)

    def get_success_url(self):
        return reverse('projects:project-settings', args=[self.object.slug])


@method_decorator(login_required, name='dispatch')
class ProjectDeleteView(SuccessDeleteMessageMixin, DeleteView):
    """ """
    model = Project
    success_url = reverse_lazy('projects:project-list')
    success_message = _("%(title)s was deleted successfully")

    def get_queryset(self):
        return self.model._default_manager.author(self.request.user)


class ProjectBadgeUrlView(View):
    """ """

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        style = self.request.GET.get('style', 'flat-square')
        project = Project.objects.filter(slug=slug).first()
        if not project:
            url = BADGE_URL.format(
                status="unknown", color='lightgrey', style=style)
            return redirect(url)
        url = BADGE_URL.format(
            status="latest", color='brightgreen', style=style)
        return redirect(url)
