# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from accounts.templatetags.accounts_tags import get_providers_unconnected


class GetProvidersUnconnectedTest(SimpleTestCase):
    """ """

    def setUp(self):
        self.providers_available = [Mock(id='prov1'), Mock(id='prov2')]

    @patch('accounts.templatetags.accounts_tags.providers')
    @patch('accounts.templatetags.accounts_tags.SocialAccount')
    def test_providers_unconnected(self, msocial, mproviders):
        msocial.objects.filter().values_list.return_value = ['prov1']
        mproviders.registry.get_list.return_value = self.providers_available
        result = get_providers_unconnected('user')
        self.assertEqual(result, [self.providers_available[1]])

    @patch('accounts.templatetags.accounts_tags.providers')
    @patch('accounts.templatetags.accounts_tags.SocialAccount')
    def test_no_providers_unconnected(self, msocial, mproviders):
        msocial.objects.filter().values_list.return_value = ['prov1', 'prov2']
        mproviders.registry.get_list.return_value = self.providers_available
        result = get_providers_unconnected('user')
        self.assertEqual(result, [])
