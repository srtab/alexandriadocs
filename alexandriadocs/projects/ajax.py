# -*- coding: utf-8 -*-
from accounts.mixins import HasAccessLevelMixin
from accounts.models import AccessLevel
from ajax_cbv.mixins import AjaxResponseAction
from ajax_cbv.views import CreateAjaxView, DeleteAjaxView, UpdateAjaxView
from core.mixins import SuccessDeleteMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from projects.forms import (
    ImportedArchiveForm, ProjectCollaboratorForm, ProjectVisibilityForm)
from projects.models import ImportedArchive, Project, ProjectCollaborator


@method_decorator(login_required, name='dispatch')
class ProjectVisibilityUpdateView(HasAccessLevelMixin, SuccessMessageMixin,
                                  UpdateAjaxView):
    """ """
    model = Project
    form_class = ProjectVisibilityForm
    success_message = _("Visibility level updated successfully")
    action = AjaxResponseAction.REFRESH
    allowed_access_level = AccessLevel.OWNER

    def get_queryset(self):
        return self.model._default_manager.collaborate(self.request.user)


class ProjectSubViewMixin(HasAccessLevelMixin):
    """ """
    project_url_kwarg = 'project_slug'
    action = AjaxResponseAction.REFRESH
    allowed_access_level = AccessLevel.ADMIN

    @cached_property
    def project(self):
        project_slug = self.kwargs.get(self.project_url_kwarg)
        projects = Project._default_manager.collaborate(self.request.user)
        return get_object_or_404(projects, slug=project_slug)

    def access_object(self):
        return self.project


@method_decorator(login_required, name='dispatch')
class ImportedArchiveCreateView(SuccessMessageMixin, ProjectSubViewMixin,
                                CreateAjaxView):
    """ """
    model = ImportedArchive
    form_class = ImportedArchiveForm
    success_message = _("Archive uploaded successfully")

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        form.instance.project = self.project
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProjectCollaboratorCreateView(SuccessMessageMixin, ProjectSubViewMixin,
                                    CreateAjaxView):
    """ """
    model = ProjectCollaborator
    form_class = ProjectCollaboratorForm
    success_message = _("%(user)s added successfully")

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProjectCollaboratorDeleteView(SuccessDeleteMessageMixin,
                                    ProjectSubViewMixin, DeleteAjaxView):
    """ """
    model = ProjectCollaborator
    success_message = _("Collaborator deleted successfully")

    def get_queryset(self):
        return self.project.project_collaborators.all()
