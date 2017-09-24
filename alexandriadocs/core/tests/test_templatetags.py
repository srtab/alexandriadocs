# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch

from core.tests.utils import TemplateTagsTest
from django.test import RequestFactory, SimpleTestCase


class IsCurrentUrlTagTest(TemplateTagsTest, SimpleTestCase):
    """ """

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/test/')
        self.request.resolver_match = Mock(url_name="dummy", namespace="dummy")

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


class BodyClassTagTest(TemplateTagsTest, SimpleTestCase):
    """ """

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/test/')

    def test_with_namespace(self):
        self.request.resolver_match = Mock(
            namespace='namespace', url_name='url_name')
        template = "{% load core_tags %}{% body_class %}"
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, 'view-namespace-url_name')

    def test_without_namespace(self):
        self.request.resolver_match = Mock(namespace=None, url_name='url_name')
        template = "{% load core_tags %}{% body_class %}"
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, 'view-url_name')


class VisibilityIconTagTest(TemplateTagsTest, SimpleTestCase):
    """ """

    def test_private_visibility(self):
        template = "{% load core_tags %}{% visibility_icon object %}"
        rendered = self.render_template(template, {
            'object': Mock(is_private=True)
        })
        expected = (
            "<span data-toggle='tooltip' data-placement='left' title='Private'"
            "><i class='fa fa-user-secret' aria-hidden='true'></i>"
            "</span>"
        )
        self.assertHTMLEqual(rendered, expected)

    def test_public_visibility(self):
        template = "{% load core_tags %}{% visibility_icon object %}"
        rendered = self.render_template(template, {
            'object': Mock(is_private=False)
        })
        expected = (
            "<span data-toggle='tooltip' data-placement='left' title='Public'>"
            "<i class='fa fa-globe' aria-hidden='true'></i>"
            "</span>"
        )
        self.assertHTMLEqual(rendered, expected)


class AbsoluteUriTagTest(TemplateTagsTest, SimpleTestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/test/')

    def test_absolute_uri(self):
        template = "{% load core_tags %}{% absolute_uri '/unit/' %}"
        rendered = self.render_template(template, {'request': self.request})
        self.assertEqual(rendered, 'http://testserver/unit/')
