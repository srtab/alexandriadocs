
from ajax_cbv.mixins import AjaxResponseAction
from ajax_cbv.views import CreateAjaxView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from projects.forms import ImportedArchiveForm
from projects.models import ImportedArchive, Project


@method_decorator(login_required, name='dispatch')
class ImportedArchiveCreateView(SuccessMessageMixin, CreateAjaxView):
    """ """
    model = ImportedArchive
    form_class = ImportedArchiveForm
    success_message = _("Archive uploaded successfully")
    project_url_kwarg = 'project_slug'
    action = AjaxResponseAction.REFRESH

    def get_project(self):
        project_slug = self.kwargs.get(self.project_url_kwarg)
        projects = Project._default_manager.collaborate(self.request.user)
        return get_object_or_404(projects, slug=project_slug)

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        form.instance.project = self.get_project()
        return super().form_valid(form)
