# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.tests.utils import TemplateTagsTest
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, SimpleTestCase
from mock import Mock, patch


class IsCurrentUrlTagTest(TemplateTagsTest, SimpleTestCase):
    """ """

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/test/')
        self.request.resolver_match = Mock(url_name="dummy", namespace="dummy")

    def test_improperly_configured(self):
        template = (
            "{% load core_tags %}{% is_current_url url_name='dummy' as val %}"
        )
        with self.assertRaises(ImproperlyConfigured):
            self.render_template(template)

    def test_url_name_match(self):
        template = (
            "{% load core_tags %}"
            "{% is_current_url url_name='dummy' as val %}"
            "{{val}}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "True")

    def test_url_name_unmatch(self):
        template = (
            "{% load core_tags %}"
            "{% is_current_url url_name='unit' as val %}"
            "{{val}}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "False")

    def test_namespace_match(self):
        template = (
            "{% load core_tags %}"
            "{% is_current_url namespace='dummy' as val %}"
            "{{val}}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "True")

    def test_namespace_unmatch(self):
        template = (
            "{% load core_tags %}"
            "{% is_current_url namespace='unit' as val %}"
            "{{val}}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "False")

    def test_url_name_and_namespace_match(self):
        template = (
            "{% load core_tags %}"
            "{% is_current_url url_name='dummy' namespace='dummy' as val %}"
            "{{val}}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "True")

    def test_url_name_and_namespace_unmatch(self):
        template = (
            "{% load core_tags %}"
            "{% is_current_url url_name='dummy' namespace='unit' as val %}"
            "{{val}}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "False")


class MenuActiveTagTest(TemplateTagsTest, SimpleTestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/test/')
        self.request.resolver_match = Mock(url_name="dummy", namespace="dummy")

    @patch("core.templatetags.core_tags.is_current_url", return_value=True)
    def test_match_url(self, mis_current_url):
        template = (
            "{% load core_tags %}{% menu_active url_name='dummy' %}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "active")

    @patch("core.templatetags.core_tags.is_current_url", return_value=False)
    def test_unmatch_url(self, mis_current_url):
        template = (
            "{% load core_tags %}{% menu_active url_name='unit' %}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "")

    @patch("core.templatetags.core_tags.is_current_url", return_value=True)
    def test_css_class(self, mis_current_url):
        template = (
            "{% load core_tags %}"
            "{% menu_active url_name='dummy' css_class='selected' %}"
        )
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "selected")


class QuerystringTagTest(TemplateTagsTest, SimpleTestCase):
    """ """

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/test/', {'page': 3})

    def test_improperly_configured(self):
        template = "{% load core_tags %}{% querystring order='dummy' %}"
        with self.assertRaises(ImproperlyConfigured):
            self.render_template(template)

    def test_new_argument(self):
        """ """
        template = "{% load core_tags %}{% querystring order='name' %}"
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "?page=3&amp;order=name")

    def test_update_argument(self):
        """ """
        template = "{% load core_tags %}{% querystring page='10' %}"
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, "?page=10")
