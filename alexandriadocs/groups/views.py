# -*- coding: utf-8 -*-
from core.views import SuccessDeleteMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from groups.forms import GroupForm
from groups.models import Group


@method_decorator(login_required, name='dispatch')
class GroupListView(ListView):
    """ """
    model = Group

    def get_queryset(self):
        return self.model._default_manager.author(self.request.user)


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
        return self.model._default_manager.visible(self.request.user)


@method_decorator(login_required, name='dispatch')
class GroupCollaboratorsView(DetailView):
    """ """
    model = Group
    template_name_suffix = '_collaborators'

    def get_queryset(self):
        return self.model._default_manager.author(self.request.user)


@method_decorator(login_required, name='dispatch')
class GroupSettingsView(SuccessMessageMixin, UpdateView):
    """ """
    model = Group
    form_class = GroupForm
    template_name_suffix = '_settings'
    success_message = _("%(title)s was updated successfully")

    def get_queryset(self):
        return self.model._default_manager.author(self.request.user)

    def get_success_url(self):
        return reverse('groups:group-settings', args=[self.object.slug])


@method_decorator(login_required, name='dispatch')
class GroupDeleteView(SuccessDeleteMessageMixin, DeleteView):
    """ """
    model = Group
    success_url = reverse_lazy('groups:group-list')
    success_message = _("%(title)s was deleted successfully")

    def get_queryset(self):
        return self.model._default_manager.author(self.request.user)
