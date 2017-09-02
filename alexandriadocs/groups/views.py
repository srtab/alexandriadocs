# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from groups.models import Group


@method_decorator(login_required, name='dispatch')
class GroupListView(ListView):
    """ """
    model = Group


@method_decorator(login_required, name='dispatch')
class GroupCreateView(CreateView):
    """ """
    model = Group
    fields = ('title', 'description')
    success_url = reverse_lazy('projects:group-list')
