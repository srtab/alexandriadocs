# -*- coding: utf-8 -*-
from core.forms import UntaggedFormMixin
from django import forms
from groups.models import Group


class GroupForm(UntaggedFormMixin, forms.ModelForm):
    """ """

    class Meta:
        model = Group
        fields = ('title', 'description', 'visibility_level')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'visibility_level': forms.RadioSelect
        }
