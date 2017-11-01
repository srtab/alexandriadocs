# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from django.views.generic import View

from accounts.mixins import HasAccessLevelMixin
from accounts.models import AccessLevel


class HasAccessLevelMixinTest(SimpleTestCase):

    class TestView(HasAccessLevelMixin, View):
        request = Mock()

    def setUp(self):
        self.view = self.TestView()

    @patch.object(HasAccessLevelMixin, 'get_object', return_value=Mock())
    def test_access_object(self, mget_object):
        self.view.access_object()
        mget_object.assert_called_with()

    @patch('accounts.mixins.access_checker_register')
    @patch.object(HasAccessLevelMixin, 'access_object', return_value=Mock())
    def test_test_func(self, maccess_object, mregister):
        obj = maccess_object()
        self.view.test_func()
        mregister.get_checker.assert_called_with(obj._meta.model)
        mregister.get_checker().has_access.assert_called_with(
            self.view.request.user, obj, AccessLevel.READER)
