# -*- coding: utf-8 -*-
from unittest.mock import patch, Mock

from django.test import SimpleTestCase

from core.sitemaps import (
    StaticViewSitemap, ProjectViewSitemap, GroupViewSitemap
)


class StaticViewSitemapTest(SimpleTestCase):
    """ """

    def setUp(self):
        self.sitemap = StaticViewSitemap()

    def test_items(self):
        self.assertEqual(self.sitemap.items(), [
            'homepage', 'account_login', 'account_signup',
            'account_reset_password', 'search:index', 'search:pages'
        ])

    def test_location(self):
        self.assertEqual(self.sitemap.location("homepage"), "/")


class ProjectViewSitemapTest(SimpleTestCase):
    """ """

    def setUp(self):
        self.sitemap = ProjectViewSitemap()

    @patch("core.sitemaps.Project.objects")
    def test_items(self, mobjects):
        self.sitemap.items()
        mobjects.public.assert_called_with()

    def test_lastmod(self):
        self.assertEqual(self.sitemap.lastmod(Mock(modified=10)), 10)


class GroupViewSitemapTest(SimpleTestCase):
    """ """

    def setUp(self):
        self.sitemap = GroupViewSitemap()

    @patch("core.sitemaps.Group.objects")
    def test_items(self, mobjects):
        self.sitemap.items()
        mobjects.public.assert_called_with()

    def test_lastmod(self):
        self.assertEqual(self.sitemap.lastmod(Mock(modified=10)), 10)
