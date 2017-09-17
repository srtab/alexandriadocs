# -*- coding: utf-8 -*-
from django.template import Context, Template


class TemplateTagsTest(object):

    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)
