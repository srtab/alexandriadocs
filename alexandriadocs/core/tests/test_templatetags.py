# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import Mock

from django.template import Context, Template
from django.test import SimpleTestCase, RequestFactory


class TemplateTagsTest(object):

    def render_template(self, string, context=None, request=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)


class CoreTagsTest(TemplateTagsTest, SimpleTestCase):
    """ """

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/test/')
        self.request.resolver_match = Mock(url_name="dummy", namespace="dummy")

    def test_menu_active_url_name_match(self):
        template = "{% load core_tags %}{% menu_active url_name='dummy' %}"
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "active")

    def test_menu_active_url_name_unmatch(self):
        template = "{% load core_tags %}{% menu_active url_name='unit' %}"
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "")

    def test_menu_active_namespace_match(self):
        template = "{% load core_tags %}{% menu_active namespace='dummy' %}"
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "active")

    def test_menu_active_namespace_unmatch(self):
        template = "{% load core_tags %}{% menu_active namespace='unit' %}"
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "")

    def test_menu_active_url_name_and_namespace_match(self):
        template = (
            "{% load core_tags %}"
            "{% menu_active url_name='dummy' namespace='dummy' %}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "active")

    def test_menu_active_url_name_and_namespace_unmatch(self):
        template = (
            "{% load core_tags %}"
            "{% menu_active url_name='dummy' namespace='unit' %}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "")

    def test_menu_active_css_class(self):
        template = (
            "{% load core_tags %}"
            "{% menu_active url_name='dummy' css_class='selected' %}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "selected")
