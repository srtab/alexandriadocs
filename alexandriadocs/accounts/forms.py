# -*- coding: utf-8 -*-
from allauth.account.forms import (
    ChangePasswordForm as AllauthChangePasswordForm,
    ResetPasswordForm as AllauthResetPasswordForm,
    ResetPasswordKeyForm as AllauthResetPasswordKeyForm,
    SetPasswordForm as AllauthSetPasswordForm,
    SignupForm as AllauthSignupForm,
)
from allauth.socialaccount.forms import SignupForm as AllauthSocialSignupForm
from core.forms import UnlabeledFormMixin, UntaggedFormMixin
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


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
