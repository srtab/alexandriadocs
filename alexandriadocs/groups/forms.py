# -*- coding: utf-8 -*-
from accounts.forms import CollaboratorForm
from core.forms import UntaggedFormMixin
from django import forms
from groups.models import Group, GroupCollaborator


class GroupForm(UntaggedFormMixin, forms.ModelForm):
    """ """

    class Meta:
        model = Group
        fields = ('title', 'description', 'visibility_level')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'visibility_level': forms.RadioSelect
        }


class GroupCollaboratorForm(CollaboratorForm):
    """ """

    class Meta(CollaboratorForm.Meta):
        model = GroupCollaborator
