# -*- coding: utf-8 -*-
from django.test import SimpleTestCase

from accounts.forms import ChangePasswordForm


class ChangePasswordFormTest(SimpleTestCase):

    def test_oldpassword_help_text(self):
        form = ChangePasswordForm()
        self.assertEqual(
            form.fields['oldpassword'].help_text,
            'You must provide your current password in order to change it.')
