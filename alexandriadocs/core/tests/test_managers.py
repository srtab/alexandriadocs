# -*- coding: utf-8 -*-
from core.managers import (
    AuthorQuerySet, AuthorVisibilityQuerySet, VisibilityQuerySet)
from core.models import VisibilityMixin
from django.test import SimpleTestCase
from mock import Mock, patch


class VisibilityQuerySetTest(SimpleTestCase):

    def setUp(self):
        self.model = VisibilityMixin

    @patch.object(VisibilityQuerySet, 'filter')
    def test_private(self, mfilter):
        queryset = VisibilityQuerySet(model=self.model)
        queryset.private()
        mfilter.assert_called_with(visibility_level=self.model.Level.PRIVATE)

    @patch.object(VisibilityQuerySet, 'filter')
    def test_public(self, mfilter):
        queryset = VisibilityQuerySet(model=self.model)
        queryset.public()
        mfilter.assert_called_with(visibility_level=self.model.Level.PUBLIC)


class AuthorQuerySetTest(SimpleTestCase):

    @patch.object(AuthorQuerySet, 'filter')
    def test_author(self, mfilter):
        AuthorQuerySet().author(None)
        mfilter.assert_called_with(author=None)


class AuthorVisibilityQuerySetTest(SimpleTestCase):

    @patch.object(AuthorVisibilityQuerySet, 'public')
    def test_visible_with_no_user(self, mpublic):
        AuthorVisibilityQuerySet().visible(None)
        mpublic.assert_called_with()

    @patch.object(AuthorVisibilityQuerySet, 'public')
    def test_visible_with_unauthenticated_user(self, mpublic):
        user = Mock(is_authenticated=False)
        AuthorVisibilityQuerySet().visible(user)
        mpublic.assert_called_with()

    @patch.object(AuthorVisibilityQuerySet, 'filter')
    def test_visible_with_authenticated_user(self, mfilter):
        user = Mock(is_authenticated=True)
        AuthorVisibilityQuerySet(model=VisibilityMixin()).visible(user)
        mfilter.assert_called_once()
