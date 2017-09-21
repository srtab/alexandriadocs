# -*- coding: utf-8 -*-
from accounts.mixins import HasAccessLevelMixin
from accounts.models import AccessLevel
from ajax_cbv.mixins import AjaxResponseAction
from ajax_cbv.views import CreateAjaxView, DeleteAjaxView, UpdateAjaxView
from core.mixins import SuccessDeleteMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from groups.forms import GroupCollaboratorForm, GroupVisibilityForm
from groups.models import Group, GroupCollaborator


@method_decorator(login_required, name='dispatch')
class GroupVisibilityUpdateView(HasAccessLevelMixin, SuccessMessageMixin,
                                UpdateAjaxView):
    """ """
    model = Group
    form_class = GroupVisibilityForm
    success_message = _("Visibility level updated successfully")
    action = AjaxResponseAction.REFRESH
    allowed_access_level = AccessLevel.OWNER

    def get_queryset(self):
        return self.request.user.collaborate_groups.all()


class GroupSubViewMixin(object):
    """ """
    group_slug_url_kwarg = 'group_slug'
    action = AjaxResponseAction.REFRESH

    def get_group(self):
        groups = self.request.user.collaborate_groups
        group_slug = self.kwargs.get(self.group_slug_url_kwarg)
        return get_object_or_404(groups, slug=group_slug)


@method_decorator(login_required, name='dispatch')
class GroupCollaboratorCreateView(SuccessMessageMixin, GroupSubViewMixin,
                                  CreateAjaxView):
    """ """
    model = GroupCollaborator
    form_class = GroupCollaboratorForm
    success_message = _("%(user)s added successfully")

    def form_valid(self, form):
        form.instance.group = self.get_group()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class GroupCollaboratorDeleteView(SuccessDeleteMessageMixin, GroupSubViewMixin,
                                  DeleteAjaxView):
    """ """
    model = GroupCollaborator
    success_message = _("Collaborator deleted successfully")
    owner_needed_message = _('The group need to have at least one owner')

    def get_queryset(self):
        return self.get_group().group_collaborators.all()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_owner or \
                self.object.is_owner and self.get_queryset().can_delete():
            return super().delete(request, *args, **kwargs)
        messages.warning(self.request, self.owner_needed_message)
        return self.json_to_response()
