# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import Context, Template


class TemplateTagsTest(object):

    def render_template(self, string, context=None, request=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)
