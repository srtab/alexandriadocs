# -*- coding: utf-8 -*-
from accounts.mixins import HasAccessLevelMixin
from accounts.models import AccessLevel
from core.mixins import SuccessDeleteMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    BaseCreateView, BaseDeleteView, CreateView, DeleteView, UpdateView)
from django.views.generic.list import ListView
from groups.forms import GroupCollaboratorForm, GroupForm
from groups.models import Group, GroupCollaborator


@method_decorator(login_required, name='dispatch')
class GroupListView(ListView):
    """ """
    model = Group

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

    def post(self, request, *args, **kwargs):
        if 'action_add' in self.request.POST:
            return self.action_add(request, *args, **kwargs)
        elif 'action_remove' in self.request.POST:
            return self.action_remove(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def action_add(self, request, *args, **kwargs):
        view = GroupCollaboratorCreateView.as_view(group=self.get_object())
        form_or_response = view(request)
        if isinstance(form_or_response, GroupCollaboratorForm):
            return self.render_to_response(
                self.get_context_data(form=form_or_response))
        return form_or_response

    def action_remove(self, request, *args, **kwargs):
        collaborator_pk = request.POST.get('collaborator_pk', None)
        view = GroupCollaboratorDeleteView.as_view(group=self.get_object())
        return view(request, pk=collaborator_pk)


class GroupCollaboratorCreateView(BaseCreateView):
    """ """
    model = GroupCollaborator
    form_class = GroupCollaboratorForm
    success_message = _("%(user)s added successfully")
    group = None

    def form_invalid(self, form):
        return form

    def form_valid(self, form):
        form.instance.group = self.group
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('groups:group-collaborators', args=[self.group.slug])


@method_decorator(login_required, name='dispatch')
class GroupCollaboratorDeleteView(SuccessDeleteMessageMixin, BaseDeleteView):
    """ """
    model = GroupCollaborator
    success_message = _("Collaborator was deleted successfully")
    group = None

    def get_queryset(self):
        return self.group.group_collaborators.all()

    def get_success_url(self):
        return reverse('groups:group-collaborators', args=[self.group.slug])


@method_decorator(login_required, name='dispatch')
class GroupSettingsView(HasAccessLevelMixin, SuccessMessageMixin, UpdateView):
    """ """
    model = Group
    form_class = GroupForm
    template_name_suffix = '_settings'
    success_message = _("%(title)s was updated successfully")
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.request.user.collaborate_groups.all()

    def get_success_url(self):
        return reverse('groups:group-settings', args=[self.object.slug])


@method_decorator(login_required, name='dispatch')
class GroupDeleteView(HasAccessLevelMixin, SuccessDeleteMessageMixin,
                      DeleteView):
    """ """
    model = Group
    success_url = reverse_lazy('groups:group-list')
    success_message = _("%(title)s was deleted successfully")
    allowed_access_level = AccessLevel.OWNER

    def get_queryset(self):
        return self.request.user.collaborate_groups.all()
