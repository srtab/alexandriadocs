# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.list import BaseListView

from core.conf import settings
from meta.views import MetadataMixin
from projects.models import Project


class AlexandriaDocsSEO(MetadataMixin):
    """ """

    def get_meta_title(self, context=None):
        base_title = "AlexandriaDocs"
        if self.title:
            return "{} — {}".format(self.title, base_title)
        return base_title

    def get_meta_url(self, context=None):
        return self.request.build_absolute_uri()

    def get_meta_description(self, context=None):
        return _(
            "AlexandriaDocs is where you can host all your documentation, "
            "making it groupable and fully searchable by you and others. "
            "You can upload your static site generated with your favorite "
            "tools like Sphinx, MkDocs, Jekyll, Hugo..."
        )


class HomepageView(AlexandriaDocsSEO, ListView):
    """ """
    model = Project
    template_name = "homepage.html"
    paginate_by = settings.ALEXANDRIA_PAGINATE_BY

    def get_queryset(self):
        return self.model._default_manager.public()


class BaseSelect2View(BaseListView):
    """ """
    paginate_by = settings.ALEXANDRIA_AUTOCOMPLETE_RESULTS

    def dispatch(self, request, *args, **kwargs):
        self.term = request.GET.get('term', None)
        return super().dispatch(request, *args, **kwargs)

    def get_options(self, context):
        return [{
            'id': str(result.pk),
            'text': str(result),
        } for result in context['object_list']]

    def render_to_response(self, context):
        """Return a JSON response in Select2 format."""
        return JsonResponse({
            'results': self.get_options(context),
            'pagination': {
                'more': context['page_obj'].has_next()
            }
        })
