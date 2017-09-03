# -*- coding: utf-8 -*-
from core.managers import VisibilityQuerySet
from core.models import VisibilityMixin
from django.test import SimpleTestCase
from mock import patch


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
