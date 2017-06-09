# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from haystack.generic_views import SearchView

from projects.models import Project, ImportedFile

from .forms import SearchForm


class SearchMixin(object):
    """ """
    template_name = "search/index.html"
    form_class = SearchForm
    search_model = None

    def get_queryset(self):
        """Filter queryset to only show results from Project models"""
        qs = super(SearchView, self).get_queryset()
        if self.search_model:
            return qs.models(self.search_model)
        return qs

    def get_context_data(self, **kwargs):
        """Add countings of projects and pages to context data"""
        context = super(SearchView, self).get_context_data(**kwargs)
        original_qs = super(SearchView, self).get_queryset()
        context.update({
            'projects_count': original_qs.models(Project).count(),
            'pages_count': original_qs.models(ImportedFile).count()
        })
        return context


class SearchProjectView(SearchMixin, SearchView):
    """ """
    search_model = Project


class SearchPageView(SearchMixin, SearchView):
    """ """
    search_model = ImportedFile
