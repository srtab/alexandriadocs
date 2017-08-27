# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from accounts.forms import ChangePasswordForm, CleanFormHelperMixin, SignupForm
from crispy_forms.helper import FormHelper
from django.test import SimpleTestCase


class ChangePasswordFormTest(SimpleTestCase):

    def test_oldpassword_help_text(self):
        form = ChangePasswordForm()
        self.assertEqual(
            form.fields['oldpassword'].help_text,
            'You must provide your current password in order to change it.')


class CleanFormHelperMixinTest(SimpleTestCase):

    def test_init(self):
        form = CleanFormHelperMixin()
        self.assertIsInstance(form.helper, FormHelper)
        self.assertFalse(form.helper.form_show_labels)
        self.assertFalse(form.helper.form_tag)


class SignupFormTest(SimpleTestCase):

    def test_init(self):
        form = SignupForm()
        self.assertIsInstance(form.helper, FormHelper)
        self.assertFalse(form.helper.form_tag)
