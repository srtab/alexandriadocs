# -*- coding: utf-8 -*-
from accounts.models import AccessLevel, CollaboratorMixin, User
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


class CollaboratorMixinTest(SimpleTestCase):

    def test_str(self):
        collaborator = CollaboratorMixin(user=User(username="username"))
        self.assertEqual(str(collaborator), 'username (Reader)')

    def test_is_owner(self):
        collaborator = CollaboratorMixin(access_level=AccessLevel.OWNER)
        self.assertTrue(collaborator.is_owner)
        collaborator = CollaboratorMixin(access_level=AccessLevel.ADMIN)
        self.assertFalse(collaborator.is_owner)

    def test_is_admin(self):
        collaborator = CollaboratorMixin(access_level=AccessLevel.ADMIN)
        self.assertTrue(collaborator.is_admin)
        collaborator = CollaboratorMixin(access_level=AccessLevel.OWNER)
        self.assertFalse(collaborator.is_admin)

    def test_is_reader(self):
        collaborator = CollaboratorMixin(access_level=AccessLevel.READER)
        self.assertTrue(collaborator.is_reader)
        collaborator = CollaboratorMixin(access_level=AccessLevel.OWNER)
        self.assertFalse(collaborator.is_reader)
