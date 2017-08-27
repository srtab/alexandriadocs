# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from allauth.account.forms import (
    ChangePasswordForm as AllauthChangePasswordForm,
    ResetPasswordForm as AllauthResetPasswordForm,
    ResetPasswordKeyForm as AllauthResetPasswordKeyForm,
    SetPasswordForm as AllauthSetPasswordForm,
    SignupForm as AllauthSignupForm,
)
from allauth.socialaccount.forms import SignupForm as AllauthSocialSignupForm
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _


class CleanFormHelperMixin(object):
    """Mixin to avoid crispy showing fields labels and rendering de form tag"""
    def __init__(self, *args, **kwargs):
        super(CleanFormHelperMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = False


class ChangePasswordForm(CleanFormHelperMixin, AllauthChangePasswordForm):
    """ """

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].help_text = _(
            'You must provide your current password in order to change it.')


class ResetPasswordForm(CleanFormHelperMixin, AllauthResetPasswordForm):
    """ """


class ResetPasswordKeyForm(CleanFormHelperMixin, AllauthResetPasswordKeyForm):
    """ """


class SetPasswordForm(CleanFormHelperMixin, AllauthSetPasswordForm):
    """ """


class SignupForm(AllauthSignupForm):
    """ """

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class SocialSignupForm(AllauthSocialSignupForm):
    """ """

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
