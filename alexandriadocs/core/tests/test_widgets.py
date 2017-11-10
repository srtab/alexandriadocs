# -*- coding: utf-8 -*-
from django.test import SimpleTestCase

from core.widgets import Select2


class Select2MixinTest(SimpleTestCase):
    """ """

    def test_init_args(self):
        mixin = Select2('url')
        self.assertTrue(hasattr(mixin, 'url'))
        self.assertEqual(mixin.url, 'url')

    def test_build_attrs_with_url(self):
        mixin = Select2('url')
        attrs = mixin.build_attrs({})
        self.assertDictEqual(attrs, {'data-autocomplete-url': 'url'})

    def test_build_attrs_without_url(self):
        mixin = Select2()
        attrs = mixin.build_attrs({})
        self.assertDictEqual(attrs, {})
