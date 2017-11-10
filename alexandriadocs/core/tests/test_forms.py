# -*- coding: utf-8 -*-
from django.test import SimpleTestCase

from core.forms import UnlabeledFormMixin, UntaggedFormMixin
from crispy_forms.helper import FormHelper


class UnlabeledFormMixinTest(SimpleTestCase):

    def test_init(self):
        form = UnlabeledFormMixin()
        self.assertIsInstance(form.helper, FormHelper)
        self.assertFalse(form.helper.form_show_labels)

    def test_init_with_helper_already_defined(self):
        setattr(UnlabeledFormMixin, 'helper', FormHelper())
        form = UnlabeledFormMixin()
        self.assertIsInstance(form.helper, FormHelper)
        self.assertFalse(form.helper.form_show_labels)


class UntaggedFormMixinTest(SimpleTestCase):

    def test_init(self):
        form = UntaggedFormMixin()
        self.assertIsInstance(form.helper, FormHelper)
        self.assertFalse(form.helper.form_tag)

    def test_init_with_helper_already_defined(self):
        setattr(UntaggedFormMixin, 'helper', FormHelper())
        form = UntaggedFormMixin()
        self.assertIsInstance(form.helper, FormHelper)
        self.assertFalse(form.helper.form_tag)
