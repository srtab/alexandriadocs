# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from groups.managers import GroupQuerySet
from groups.models import Group


class GroupQuerySetTest(SimpleTestCase):

    def setUp(self):
        self.queryset = GroupQuerySet(model=Group)

    @patch.object(GroupQuerySet, 'filter')
    def test_public(self, mfilter):
        self.queryset.public()
        mfilter.assert_called_with(visibility_level=Group.Level.PUBLIC)

    @patch.object(GroupQuerySet, 'public')
    def test_public_and_collaborate_with_no_user(self, mpublic):
        self.queryset.public_and_collaborate()
        mpublic.assert_called_once_with()

    @patch.object(GroupQuerySet, 'public')
    def test_public_and_collaborate_with_unauthenticated_user(self, mpublic):
        user = Mock(is_authenticated=False)
        self.queryset.public_and_collaborate(user)
        mpublic.assert_called_once_with()

    @patch.object(GroupQuerySet, 'filter')
    def test_public_and_collaborate_with_authenticated_user(self, mfilter):
        user = Mock(is_authenticated=True)
        self.queryset.public_and_collaborate(user)
        user.collaborate_groups.values.assert_called_with('pk')
        self.assertTrue(mfilter.called)
