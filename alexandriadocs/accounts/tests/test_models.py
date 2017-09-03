# -*- coding: utf-8 -*-
from accounts.models import User
from django.test import SimpleTestCase
from django.urls import reverse


class UserModelTest(SimpleTestCase):

    def test_str(self):
        user = User(username="username")
        self.assertEqual(str(user), user.username)

    def test_get_absolute_url(self):
        user = User(slug="slug")
        expected = reverse('accounts:index', args=['slug'])
        self.assertEqual(expected, user.get_absolute_url())
