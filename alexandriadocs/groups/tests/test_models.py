# -*- coding: utf-8 -*-
from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import reverse

from accounts.models import AccessLevel
from groups.models import Group, GroupCollaborator


class GroupModelTest(SimpleTestCase):

    def test_str(self):
        group = Group(name="name")
        self.assertEqual(str(group), group.name)

    def test_get_absolute_url(self):
        group = Group(slug="name")
        expected = reverse('groups:group-detail', args=[group.slug])
        self.assertEqual(expected, group.get_absolute_url())

    @patch.object(GroupCollaborator, 'objects')
    def test_post_save_with_created_true(self, mobjects):
        Group.post_save(Group, Group(pk=1, author_id=1), True)
        mobjects.create.assert_called_with(
            group_id=1, user_id=1, access_level=AccessLevel.OWNER)

    @patch.object(GroupCollaborator, 'objects')
    def test_post_save_with_created_false(self, mobjects):
        Group.post_save(Group, None, False)
        mobjects.create.assert_not_called()
