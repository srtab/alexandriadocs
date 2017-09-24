# -*- coding: utf-8 -*-
from django.template import Context, Template


class TemplateTagsTest(object):

    def render_template(self, string, context=None):
        context = Context(context or {})
        return Template(string).render(context)
