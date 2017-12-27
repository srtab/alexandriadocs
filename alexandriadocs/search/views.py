# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView

from core.views import AlexandriaDocsSEO
from haystack.inputs import Clean
from haystack.query import SQ, EmptySearchQuerySet, RelatedSearchQuerySet
from projects.models import ImportedFile, Project


class SearchView(ListView):
    """ """
    template_name = "search/index.html"
    search_model = None
    search_field = 'q'
    paginate_by = 20

    def get_query(self):
        return self.request.GET.get(self.search_field, "")

    def get_queryset(self):
        return self.search(self.get_query()).models(self.search_model)\
            .load_all()

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        queryset = self.search(self.get_query())
        context.update({
            'query': self.get_query(),
            'projects_count': queryset.models(Project).count(),
            'pages_count': queryset.models(ImportedFile).count()
        })
        return context

    def search(self, query):
        if not query:
            return EmptySearchQuerySet()
        # OPTIMIZE: the number of public projects can increase substantially
        # causing a really high number of project_ids to be sended to
        # elasticsearch
        projects = Project.objects.public_or_collaborate(self.request.user)
        return RelatedSearchQuerySet()\
            .filter(project_id__in=projects.values_list('pk', flat=True))\
            .filter(SQ(content__contains=Clean(query)) |
                    SQ(title__contains=Clean(query)))


class SearchProjectView(AlexandriaDocsSEO, SearchView):
    """ """
    search_model = Project
    title = _("Search for projects")

    def get_meta_description(self, context=None):
        return _("Explore available projects")


class SearchPageView(AlexandriaDocsSEO, SearchView):
    """ """
    search_model = ImportedFile
    title = _("Search for docs")

    def get_meta_description(self, context=None):
        return _("Explore available documentations pages")
