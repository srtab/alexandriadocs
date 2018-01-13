# -*- coding: utf-8 -*-
from unittest.mock import patch, Mock

from django.test import SimpleTestCase

from api.permissions import HasAPIAccess


class HasAPIAccessTest(SimpleTestCase):

    def test_has_permission_empty_meta(self):
        request = Mock(META={})
        self.assertFalse(HasAPIAccess().has_permission(request, None))

    @patch("api.permissions.token_generator.check_token", return_value=False)
    def test_has_permission_token_invalid(self, mtoken_generator):
        request = Mock(META={'HTTP_API_KEY': 'token'})
        self.assertFalse(HasAPIAccess().has_permission(request, None))

    @patch("api.permissions.token_generator.check_token", return_value=True)
    def test_has_permission_token_valid(self, mtoken_generator):
        request = Mock(META={'HTTP_API_KEY': 'token'})
        self.assertTrue(HasAPIAccess().has_permission(request, None))
