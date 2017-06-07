# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from haystack.generic_views import SearchView

from projects.models import Project

from .forms import SearchForm


class SearchView(SearchView):
    """ """
    template_name = "search/index.html"
    form_class = SearchForm

    def get_queryset(self):
        """
        Filter queryset to only show results from Project models
        """
        sqs = super(SearchView, self).get_queryset()
        return sqs.models(Project)
