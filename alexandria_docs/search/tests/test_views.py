# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase


class SearchViewTest(TestCase):

    def setUp(self):
        self.url = reverse('search:index')

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("search/index.html")
