# -*- coding: utf-8 -*-
from accounts.mixins import HasAccessLevelMixin
from accounts.models import AccessLevel
from core.mixins import SuccessDeleteMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from projects.forms import ImportedArchiveForm, ProjectEditForm, ProjectForm
from projects.models import ImportedArchive, Project


BADGE_URL = (
    'https://img.shields.io/badge/docs-{status}-{color}.svg?style={style}'
)


@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    """ """
    model = Project

    def get_queryset(self):
        return self.request.user.collaborate_projects.all()


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(HasAccessLevelMixin, SuccessMessageMixin, CreateView):
    """ """
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects:project-list')
    success_message = _("%(title)s was created successfully")
    allowed_access_level = AccessLevel.ADMIN

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    """ """
    model = Project

    def get_queryset(self):
        return self.model._default_manager.public_and_collaborate(
            self.request.user)


class ProjectBadgeView(DetailView):
    """ """
    model = Project
    template_name_suffix = '_badge'


@method_decorator(login_required, name='dispatch')
class ProjectCollaboratorsView(HasAccessLevelMixin, DetailView):
    """ """
    model = Project
    template_name_suffix = '_collaborators'
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.request.user.collaborate_projects.all()


@method_decorator(login_required, name='dispatch')
class ProjectSettingsView(HasAccessLevelMixin, SuccessMessageMixin,
                          UpdateView):
    """ """
    model = Project
    form_class = ProjectEditForm
    template_name_suffix = '_settings'
    success_message = _("%(title)s was updated successfully")
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.request.user.collaborate_projects.all()

    def get_success_url(self):
        return reverse('projects:project-settings', args=[self.object.slug])


@method_decorator(login_required, name='dispatch')
class ProjectDeleteView(HasAccessLevelMixin, SuccessDeleteMessageMixin,
                        DeleteView):
    """ """
    model = Project
    success_url = reverse_lazy('projects:project-list')
    success_message = _("%(title)s was deleted successfully")
    allowed_access_level = AccessLevel.OWNER

    def get_queryset(self):
        return self.request.user.collaborate_projects.all()


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


@method_decorator(login_required, name='dispatch')
class ProjectImportedArchiveView(HasAccessLevelMixin, CreateView):
    """ """
    model = ImportedArchive
    form_class = ImportedArchiveForm
    template_name = 'projects/project_imported_archives.html'
    success_url = reverse_lazy('projects:project-imported-archive')
    success_message = _("Archive uploaded successfully")
    project_url_kwarg = 'slug'
    allowed_access_level = AccessLevel.ADMIN

    def get_project(self):
        project_slug = self.kwargs.get(self.project_url_kwarg)
        collaborate_projects = self.request.user.collaborate_projects.all()
        return get_object_or_404(collaborate_projects, slug=project_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'project': self.get_project(),
        })
        return context

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        form.instance.project = self.get_project()
        return super().form_valid(form)

    def get_success_url(self):
        project_slug = self.kwargs.get(self.project_url_kwarg)
        return reverse(
            'projects:project-imported-archive', args=[project_slug])
