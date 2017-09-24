# -*- coding: utf-8 -*-
from unittest.mock import patch

from accounts.managers import CollaboratorQuerySet
from accounts.models import AccessLevel
from django.test import SimpleTestCase


class CollaboratorManagerTest(SimpleTestCase):

    @patch.object(CollaboratorQuerySet, 'filter')
    def test_can_delete(self, mfilter):
        mfilter().count.return_value = 0
        self.assertFalse(CollaboratorQuerySet().can_delete())
        mfilter.assert_called_with(access_level=AccessLevel.OWNER)
        mfilter().count.assert_called_with()

    @patch.object(CollaboratorQuerySet, 'filter')
    def test_can_delete_with_min_count(self, mfilter):
        mfilter().count.return_value = 1
        self.assertFalse(CollaboratorQuerySet().can_delete())
        mfilter().count.return_value = 2
        self.assertTrue(CollaboratorQuerySet().can_delete())
