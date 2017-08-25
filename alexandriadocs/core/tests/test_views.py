# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse


class HomepageTest(TestCase):

    def setUp(self):
        self.url = reverse('homepage')

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("homepage.html")
