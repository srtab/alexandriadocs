# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.generic.list import BaseListView
from projects.models import Project


class HomepageView(ListView):
    """ """
    template_name = "homepage.html"
    model = Project
    paginate_by = 10

    def get_queryset(self):
        return self.model._default_manager.public()


class BaseSelect2View(BaseListView):
    """ """
    paginate_by = 10

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
