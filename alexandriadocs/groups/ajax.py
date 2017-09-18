from ajax_cbv.mixins import AjaxResponseAction
from ajax_cbv.views import CreateAjaxView, DeleteAjaxView
from core.mixins import SuccessDeleteMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from groups.forms import GroupCollaboratorForm
from groups.models import GroupCollaborator


class GroupSubViewMixin(object):
    """ """
    group_slug_url_kwarg = 'group_slug'

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
    action = AjaxResponseAction.REFRESH

    def form_valid(self, form):
        form.instance.group = self.get_group()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class GroupCollaboratorDeleteView(SuccessDeleteMessageMixin, GroupSubViewMixin,
                                  DeleteAjaxView):
    """ """
    model = GroupCollaborator
    success_message = _("Collaborator deleted successfully")
    action = AjaxResponseAction.REFRESH

    def get_queryset(self):
        return self.get_group().group_collaborators.all()
