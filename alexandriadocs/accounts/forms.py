# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import \
    ChangePasswordForm as AllauthChangePasswordForm
from allauth.account.forms import ResetPasswordForm as AllauthResetPasswordForm
from allauth.account.forms import \
    ResetPasswordKeyForm as AllauthResetPasswordKeyForm
from allauth.account.forms import SetPasswordForm as AllauthSetPasswordForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.socialaccount.forms import SignupForm as AllauthSocialSignupForm
from core.forms import UnlabeledFormMixin, UntaggedFormMixin
from core.widgets import Select2


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


class CollaboratorForm(UntaggedFormMixin, forms.ModelForm):
    """ """

    class Meta:
        fields = ('user', 'access_level')
        widgets = {
            'user': Select2(url=reverse_lazy('accounts:user-search'))
        }
