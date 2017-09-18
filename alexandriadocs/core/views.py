# -*- coding: utf-8 -*-
from django.views.generic import ListView

from projects.models import Project


class HomepageView(ListView):
    """ """
    template_name = "homepage.html"
    model = Project
    paginate_by = 10

    def get_queryset(self):
        return self.model._default_manager.public()
