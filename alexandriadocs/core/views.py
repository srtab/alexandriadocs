# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views.generic import ListView

from projects.models import Project


class HomepageView(ListView):
    """ """
    template_name = "homepage.html"
    model = Project
    paginate_by = 3 * 5  # elems per line * num lines


class SuccessDeleteMessageMixin(object):

    def delete(self, request, *args, **kwargs):
        # SuccessMessageMixin not supported on delete views
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.get_success_message())
        return response

    def get_success_message(self):
        return self.success_message % self.object.__dict__
