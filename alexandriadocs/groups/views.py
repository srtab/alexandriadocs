# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from groups.forms import GroupForm
from groups.models import Group


@method_decorator(login_required, name='dispatch')
class GroupListView(ListView):
    """ """
    model = Group

    def get_queryset(self):
        return self.model._default_manager.filter(author=self.request.user)


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
