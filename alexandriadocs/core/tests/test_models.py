# -*- coding: utf-8 -*-
from core.models import VisibilityMixin
from django.test import SimpleTestCase


class VisibilityMixinTest(SimpleTestCase):

    def test_is_private(self):
        visibility = VisibilityMixin()
        self.assertTrue(visibility.is_private)
        visibility = VisibilityMixin(
            visibility_level=VisibilityMixin.Level.PUBLIC)
        self.assertFalse(visibility.is_private)

    def test_is_public(self):
        visibility = VisibilityMixin(
            visibility_level=VisibilityMixin.Level.PUBLIC)
        self.assertTrue(visibility.is_public)
        visibility = VisibilityMixin()
        self.assertFalse(visibility.is_public)
