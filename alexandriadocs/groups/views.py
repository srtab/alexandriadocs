# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from accounts.mixins import HasAccessLevelMixin
from accounts.models import AccessLevel
from core.conf import settings
from core.views import AlexandriaDocsSEO
from groups.forms import (
    GroupCollaboratorForm, GroupEditForm, GroupForm, GroupVisibilityForm
)
from groups.models import Group


@method_decorator(login_required, name='dispatch')
class GroupListView(AlexandriaDocsSEO, ListView):
    """ """
    model = Group
    title = _("Groups")
    paginate_by = settings.ALEXANDRIA_PAGINATE_BY

    def get_queryset(self):
        return self.request.user.collaborate_groups.all()


@method_decorator(login_required, name='dispatch')
class GroupCreateView(AlexandriaDocsSEO, SuccessMessageMixin, CreateView):
    """ """
    model = Group
    title = _("Create group")
    form_class = GroupForm
    success_message = _("%(name)s was created successfully")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GroupDetailMixin(AlexandriaDocsSEO):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'project_list': self.object.projects.collaborate(
                self.request.user)
        })
        return context

    def get_meta_description(self, context=None):
        if self.object.description:
            return self.object.description
        return None


class GroupDetailView(GroupDetailMixin, DetailView):
    """ """
    model = Group

    def get_queryset(self):
        return self.model._default_manager.public_and_collaborate(
            self.request.user)

    def get_meta_title(self, context=None):
        self.title = _("Projects · {name}").format(name=self.object)
        return super().get_meta_title(context)


@method_decorator(login_required, name='dispatch')
class GroupCollaboratorsView(HasAccessLevelMixin, GroupDetailMixin,
                             DetailView):
    """ """
    model = Group
    template_name_suffix = '_collaborators'
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.request.user.collaborate_groups.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context.update({
                'form': GroupCollaboratorForm(),
            })
        return context

    def get_meta_title(self, context=None):
        self.title = _("Collaborators · {name}").format(name=self.object)
        return super().get_meta_title(context)


@method_decorator(login_required, name='dispatch')
class GroupSettingsView(HasAccessLevelMixin, SuccessMessageMixin,
                        GroupDetailMixin, UpdateView):
    """ """
    model = Group
    form_class = GroupEditForm
    template_name_suffix = '_settings'
    success_message = _("%(name)s was updated successfully")
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.request.user.collaborate_groups.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'visibility_form': GroupVisibilityForm(instance=self.object)
        })
        return context

    def get_success_url(self):
        return reverse('groups:group-settings', args=[self.object.slug])

    def get_meta_title(self, context=None):
        self.title = _("Settings · {name}").format(name=self.object)
        return super().get_meta_title(context)
