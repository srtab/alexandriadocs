# -*- coding: utf-8 -*-
from core.forms import UntaggedFormMixin
from crispy_forms.bootstrap import PrependedText
from crispy_forms.layout import Div, Layout
from django import forms
from django.utils.translation import ugettext_lazy as _
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = _('Project name')
        self.fields['repo'].widget.attrs['placeholder'] = \
            'ex: https://github.com/srtab/alexandriadocs'
        self.fields['tags'].widget.attrs['placeholder'] = \
            'ex: django, python'

    def form_helper(self):
        super().form_helper()
        self.helper.layout = Layout(
            Div(
                Div('group', css_class="col-4"),
                Div('title', css_class="col-8"),
                css_class="row",
            ),
            'description',
            PrependedText(
                'repo', '<i class="fa fa-link" aria-hidden="true"></i>'),
            PrependedText(
                'tags', '<i class="fa fa-tag" aria-hidden="true"></i>'),
            'visibility_level'
        )


class ProjectEditForm(ProjectForm):
    """ """
    class Meta(ProjectForm.Meta):
        fields = (
            'title', 'description', 'repo', 'tags', 'visibility_level'
        )

    def form_helper(self):
        super().form_helper()
        self.helper.layout[0] = 'title'
