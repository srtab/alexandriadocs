# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls import reverse


class SearchProjectViewTest(TestCase):

    def setUp(self):
        self.url = reverse('search:index')

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("search/index.html")

    def test_search(self):
        response = self.client.get(self.url, {'q': 'serach'})
        self.assertEqual(response.status_code, 200)


class SearchPageViewTest(TestCase):

    def setUp(self):
        self.url = reverse('search:pages')

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("search/index.html")

    def test_search(self):
        response = self.client.get(self.url, {'q': 'serach'})
        self.assertEqual(response.status_code, 200)
