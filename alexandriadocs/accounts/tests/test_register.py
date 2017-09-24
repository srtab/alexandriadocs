# -*- coding: utf-8 -*-
from unittest.mock import Mock

from accounts.register import access_checker_register
from django.test import SimpleTestCase


class AccessCheckerRegistryTest(SimpleTestCase):

    def test_register(self):
        callable = Mock()
        access_checker_register.register('model', callable)
        self.assertIn('model', access_checker_register._registry)
        callable.assert_called_with()

    def test_get_checker(self):
        access_checker_register.register('model', Mock())
        self.assertIsNotNone(access_checker_register.get_checker('model'))
        self.assertIsNone(access_checker_register.get_checker('other'))
