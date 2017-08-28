# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from accounts.forms import (
    ChangePasswordForm, UnlabeledFormMixin, UntaggedFormMixin)
from crispy_forms.helper import FormHelper
from django.test import SimpleTestCase


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


class ChangePasswordFormTest(SimpleTestCase):

    def test_oldpassword_help_text(self):
        form = ChangePasswordForm()
        self.assertEqual(
            form.fields['oldpassword'].help_text,
            'You must provide your current password in order to change it.')
