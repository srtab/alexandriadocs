# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from groups.access_checkers import group_access_checker


class GroupAccessCheckerTest(SimpleTestCase):

    @patch.object(group_access_checker, 'get_object', return_value=None)
    def test_has_access_no_collaborator(self, mget_object):
        self.assertFalse(group_access_checker.has_access('user', Mock(), 1))
        mget_object.assert_called_once()

    @patch.object(group_access_checker, 'get_object',
                  return_value=Mock(access_level=1))
    def test_has_access_with_collaborator(self, mget_object):
        self.assertTrue(group_access_checker.has_access('user', Mock(), 1))
        self.assertFalse(group_access_checker.has_access('user', Mock(), 2))
