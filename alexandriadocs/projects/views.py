# -*- coding: utf-8 -*-
import logging
import os

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from accounts.mixins import HasAccessLevelMixin
from accounts.models import AccessLevel
from core.conf import settings
from core.views import AlexandriaDocsSEO
from groups.models import Group
from projects.forms import (
    ImportedArchiveForm, ProjectCollaboratorForm, ProjectEditForm, ProjectForm,
    ProjectVisibilityForm
)
from projects.models import Project
from sendfile import sendfile

logger = logging.getLogger('alexandria.projects')


BADGE_URL = (
    'https://img.shields.io/badge/docs-{status}-{color}.svg?style={style}'
)


@method_decorator(login_required, name='dispatch')
class ProjectListView(AlexandriaDocsSEO, ListView):
    """ """
    model = Project
    title = _("Projects")
    paginate_by = settings.ALEXANDRIA_PAGINATE_BY

    def get_queryset(self):
        return self.model._default_manager.collaborate(self.request.user)\
            .select_related('group')


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(AlexandriaDocsSEO, SuccessMessageMixin, CreateView):
    """ """
    model = Project
    title = _("Create project")
    form_class = ProjectForm
    success_message = _("%(title)s was created successfully")

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        group_slug = self.request.GET.get('group')
        group = Group.objects.filter(slug=group_slug).values('pk').first()
        if not group:
            return {}
        return {'group': group.get('pk')}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectDetailMixin(AlexandriaDocsSEO):

    def get_queryset(self):
        return self.model._default_manager\
            .public_or_collaborate(self.request.user)\
            .select_related('group')

    def get_meta_description(self, context=None):
        if self.object.description:
            return self.object.description
        return None

    def get_meta_keywords(self, context=None):
        if self.object.tags.exists():
            return self.object.tags.values_list('name', flat=True)
        return None


class ProjectDetailView(ProjectDetailMixin, DetailView):
    """ """
    model = Project

    def get_meta_title(self, context=None):
        self.title = self.object.fullname
        return super().get_meta_title(context)


class ProjectBadgeView(ProjectDetailMixin, DetailView):
    """ """
    model = Project
    template_name_suffix = '_badge'

    def get_meta_title(self, context=None):
        self.title = _("Badge · {name}").format(name=self.object.fullname)
        return super().get_meta_title(context)


@method_decorator(login_required, name='dispatch')
class ProjectUploadsView(HasAccessLevelMixin, ProjectDetailMixin, DetailView):
    """ """
    model = Project
    template_name_suffix = '_uploads'
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.model._default_manager.collaborate(self.request.user)\
            .select_related('group')

    def get_context_data(self, **kwargs):
        limit = settings.ALEXANDRIA_UPLOADS_HISTORY_LIMIT
        context = super().get_context_data(**kwargs)
        context.update({
            'form': ImportedArchiveForm(),
            'allowed_mimetypes': settings.ALEXANDRIA_ALLOWED_MIMETYPES,
            'imported_archives': self.object.imported_archives.all()[:limit]
        })
        return context

    def get_meta_title(self, context=None):
        self.title = _("Uploads · {name}").format(name=self.object.fullname)
        return super().get_meta_title(context)


@method_decorator(login_required, name='dispatch')
class ProjectCollaboratorsView(HasAccessLevelMixin, ProjectDetailMixin,
                               DetailView):
    """ """
    model = Project
    template_name_suffix = '_collaborators'
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.model._default_manager.collaborate(self.request.user)\
            .select_related('group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': ProjectCollaboratorForm()})
        return context

    def get_meta_title(self, context=None):
        self.title = _("Collaborators · {name}").format(
            name=self.object.fullname)
        return super().get_meta_title(context)


@method_decorator(login_required, name='dispatch')
class ProjectSettingsView(HasAccessLevelMixin, SuccessMessageMixin,
                          ProjectDetailMixin, UpdateView):
    """ """
    model = Project
    form_class = ProjectEditForm
    template_name_suffix = '_settings'
    success_message = _("%(title)s was updated successfully")
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.model._default_manager.collaborate(self.request.user)\
            .select_related('group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'visibility_form': ProjectVisibilityForm(instance=self.object),
        })
        return context

    def get_success_url(self):
        return reverse('projects:project-settings', args=[self.object.slug])

    def get_meta_title(self, context=None):
        self.title = _("Settings · {name}").format(name=self.object.fullname)
        return super().get_meta_title(context)


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


class ProjectServeDocs(DetailView):
    """ """
    model = Project

    def get_queryset(self):
        return self.model._default_manager\
            .public_or_collaborate(self.request.user)\
            .select_related('group')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        path = self.kwargs.get("path", "index.html")
        filename = os.path.join(self.object.serve_root_path, path)
        if not os.path.exists(filename):
            logger.warning("Serve docs: file not found path=%s", filename)
            raise Http404("File not found")
        # handle indexes
        if filename[-1] == '/':
            filename += 'index.html'
        return sendfile(request, filename)
