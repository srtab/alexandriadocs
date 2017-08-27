# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ProfileUpdateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='unit', password='secret')
        self.url = reverse('accounts:index', args=[self.user.pk])
        self.client.force_login(self.user)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             '{}?next={}'.format(settings.LOGIN_URL, self.url))

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("accounts/index.html")

    def test_update_profile(self):
        data = {
            'username': 'test',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
