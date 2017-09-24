# -*- coding: utf-8 -*-
from unittest.mock import Mock

from accounts.access_checkers import AccessChecker
from django.core.exceptions import ObjectDoesNotExist
from django.test import SimpleTestCase


class AccessCheckerTest(SimpleTestCase):

    class TestAccessChecker(AccessChecker):
        model = Mock()
        object_field_name = 'field'

    def test_get_object(self):
        access_checker = self.TestAccessChecker()
        access_checker.get_object('user', 'obj')
        manager = access_checker.model._default_manager
        manager.only.assert_called_with('access_level')
        manager.only().get.assert_called_with(user='user', field='obj')

    def test_get_object_object_does_not_exist(self):
        access_checker = self.TestAccessChecker()
        manager = access_checker.model._default_manager
        manager.only.side_effect = ObjectDoesNotExist()
        self.assertIsNone(access_checker.get_object('user', 'obj'))

    def test_has_access(self):
        access_checker = self.TestAccessChecker()
        self.assertFalse(access_checker.has_access('user', 'obj', 'level'))

    def test_get_access_level(self):
        access_checker = self.TestAccessChecker()
        self.assertEqual(access_checker.get_access_level('user', 'obj'), 0)
