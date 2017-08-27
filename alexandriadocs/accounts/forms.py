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
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class UntaggedFormMixin(object):
    """Mixin to avoid crispy showing fields labels and rendering de form tag"""
    def __init__(self, *args, **kwargs):
        super(UntaggedFormMixin, self).__init__(*args, **kwargs)
        if not hasattr(self, 'helper'):
            self.helper = FormHelper()
        self.helper.form_tag = False


class UnlabeledFormMixin(object):
    """Mixin to avoid crispy showing fields labels and rendering de form tag"""
    def __init__(self, *args, **kwargs):
        super(UnlabeledFormMixin, self).__init__(*args, **kwargs)
        if not hasattr(self, 'helper'):
            self.helper = FormHelper()
        self.helper.form_show_labels = False


class ChangePasswordForm(UnlabeledFormMixin, UntaggedFormMixin,
                         AllauthChangePasswordForm):
    """ """

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].help_text = _(
            'You must provide your current password in order to change it.')


class ResetPasswordForm(UnlabeledFormMixin, UntaggedFormMixin,
                        AllauthResetPasswordForm):
    """ """


class ResetPasswordKeyForm(UnlabeledFormMixin, UntaggedFormMixin,
                           AllauthResetPasswordKeyForm):
    """ """


class SetPasswordForm(UnlabeledFormMixin, UntaggedFormMixin,
                      AllauthSetPasswordForm):
    """ """


class SignupForm(UntaggedFormMixin, AllauthSignupForm):
    """ """


class SocialSignupForm(UntaggedFormMixin, AllauthSocialSignupForm):
    """ """


class ProfileUpdateForm(UntaggedFormMixin, forms.ModelForm):
    """ """

    class Meta:
        model = get_user_model()
        fields = ('username', 'name')
