# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from projects.access_checkers import project_access_checker


@patch('projects.access_checkers.group_access_checker')
class ProjectAccessCheckerTest(SimpleTestCase):

    @patch.object(project_access_checker, 'get_object', return_value=None)
    def test_has_access_no_project_collab(self, mget_object, mgroup_checker):
        obj = Mock()
        mgroup_checker.has_access.return_value = False
        self.assertFalse(project_access_checker.has_access('user', obj, 1))
        self.assertTrue(mget_object.called)
        mgroup_checker.has_access.assert_called_with('user', obj.group, 1)
        mgroup_checker.has_access.return_value = True
        self.assertTrue(project_access_checker.has_access('user', obj, 1))

    @patch.object(project_access_checker, 'get_object',
                  return_value=Mock(access_level=1))
    def test_has_access_with_project_collab(self, mget_object, mgroup_checker):
        mgroup_checker.has_access.return_value = True
        self.assertTrue(project_access_checker.has_access('user', Mock(), 1))
        self.assertTrue(project_access_checker.has_access('user', Mock(), 2))
        mgroup_checker.has_access.return_value = False
        self.assertTrue(project_access_checker.has_access('user', Mock(), 1))
        self.assertFalse(project_access_checker.has_access('user', Mock(), 2))
