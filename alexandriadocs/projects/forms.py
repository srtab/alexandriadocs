# -*- coding: utf-8 -*-
from core.forms import UntaggedFormMixin
from django import forms
from projects.models import Project


class ProjectForm(UntaggedFormMixin, forms.ModelForm):
    """ """

    class Meta:
        model = Project
        fields = (
            'title', 'description', 'group', 'repo', 'tags', 'visibility_level'
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'visibility_level': forms.RadioSelect
        }
