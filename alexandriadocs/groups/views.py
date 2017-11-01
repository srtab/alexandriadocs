# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from accounts.mixins import HasAccessLevelMixin
from accounts.models import AccessLevel
from core.conf import settings
from groups.forms import (
    GroupCollaboratorForm, GroupEditForm, GroupForm, GroupVisibilityForm
)
from groups.models import Group


@method_decorator(login_required, name='dispatch')
class GroupListView(ListView):
    """ """
    model = Group
    paginate_by = settings.ALEXANDRIA_PAGINATE_BY

    def get_queryset(self):
        return self.request.user.collaborate_groups.all()


@method_decorator(login_required, name='dispatch')
class GroupCreateView(SuccessMessageMixin, CreateView):
    """ """
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('groups:group-list')
    success_message = _("%(title)s was created successfully")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GroupDetailView(DetailView):
    """ """
    model = Group

    def get_queryset(self):
        return self.model._default_manager.public_and_collaborate(
            self.request.user)


@method_decorator(login_required, name='dispatch')
class GroupCollaboratorsView(HasAccessLevelMixin, DetailView):
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


@method_decorator(login_required, name='dispatch')
class GroupSettingsView(HasAccessLevelMixin, SuccessMessageMixin, UpdateView):
    """ """
    model = Group
    form_class = GroupEditForm
    template_name_suffix = '_settings'
    success_message = _("%(title)s was updated successfully")
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
