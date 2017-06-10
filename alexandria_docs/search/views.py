# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from haystack.generic_views import SearchView as HaystackSearchView
from haystack.inputs import Clean

from projects.models import Project, ImportedFile


class SearchView(HaystackSearchView):
    """ """
    template_name = "search/index.html"
    search_model = None

    def form_valid(self, form):
        query = form.cleaned_data.get(self.search_field)
        queryset = self.search(query)
        context = self.get_context_data(**{
            self.form_name: form,
            'query': query,
            'object_list': queryset.models(self.search_model),
            'projects_count': queryset.models(Project).count(),
            'pages_count': queryset.models(ImportedFile).count()
        })
        return self.render_to_response(context)

    def search(self, query):
        return self.get_queryset().filter(content__contains=Clean(query))


class SearchProjectView(SearchView):
    """ """
    search_model = Project


class SearchPageView(SearchView):
    """ """
    search_model = ImportedFile
