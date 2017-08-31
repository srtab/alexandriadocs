# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import SimpleTestCase
from django.urls import reverse
from mock import Mock, patch
from projects.views import BADGE_URL


class SearchProjectViewTest(SimpleTestCase):

    def setUp(self):
        self.url = reverse(
            'projects:project-badge', kwargs={'project_slug': 'slug'})
        self.badge_latest = BADGE_URL.format(
            status="latest", color="brightgreen", style="flat-square")
        self.badge_unknown = BADGE_URL.format(
            status="unknown", color="lightgrey", style="flat-square")

    @patch('projects.views.Project.objects.filter', return_value=Mock())
    def test_badge(self, mfilter):
        mfilter().first.return_value = True
        response = self.client.get(self.url)
        self.assertRedirects(response, self.badge_latest,
                             fetch_redirect_response=False)

    @patch('projects.views.Project.objects.filter', return_value=Mock())
    def test_badge_not_found_project(self, mfilter):
        mfilter().first.return_value = None
        response = self.client.get(self.url)
        self.assertRedirects(response, self.badge_unknown,
                             fetch_redirect_response=False)
