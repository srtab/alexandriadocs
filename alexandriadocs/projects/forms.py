# -*- coding: utf-8 -*-
from accounts.forms import CollaboratorForm
from accounts.models import AccessLevel
from core.forms import UntaggedFormMixin
from crispy_forms.bootstrap import PrependedText
from crispy_forms.layout import Div, Layout
from django import forms
from django.utils.translation import ugettext_lazy as _
from groups.access_checkers import group_access_checker
from projects.models import ImportedArchive, Project, ProjectCollaborator


PROJECT_COMMON_FIELDS = ('title', 'description', 'repo', 'tags')


class ProjectForm(UntaggedFormMixin, forms.ModelForm):
    """ """
    error_messages = {
        'permission_denied': _(
            "You don\'t have permissions to create projects in the "
            "group %(group)s."
        )
    }

    class Meta:
        model = Project
        fields = PROJECT_COMMON_FIELDS + ('group', 'visibility_level')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'visibility_level': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['title'].label = _('Project name')
        self.fields['repo'].widget.attrs['placeholder'] = \
            'ex: https://github.com/srtab/alexandriadocs'
        self.fields['tags'].widget.attrs['placeholder'] = 'ex: django, python'

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

    def clean_group(self):
        group = self.cleaned_data.get('group')
        has_access = group_access_checker.has_access(
            self.user, group, AccessLevel.ADMIN)
        if not has_access:
            raise forms.ValidationError(
                self.error_messages['permission_denied'],
                code='permission_denied',
                params={'group': group},
            )
        return group


class ProjectEditForm(ProjectForm):
    """ """
    class Meta(ProjectForm.Meta):
        fields = PROJECT_COMMON_FIELDS
        widgets = {
            'description': ProjectForm.Meta.widgets['description'],
        }

    def form_helper(self):
        super().form_helper()
        # remove row element with group an title an replace by title only
        self.helper.layout[0] = 'title'
        # remove visibility_level
        del self.helper.layout[-1]


class ProjectVisibilityForm(UntaggedFormMixin, forms.ModelForm):
    """ """
    class Meta:
        model = Project
        fields = ('visibility_level',)
        widgets = {
            'visibility_level': ProjectForm.Meta.widgets['visibility_level'],
        }

    def form_helper(self):
        super().form_helper()
        self.helper.form_show_labels = False


class ImportedArchiveForm(UntaggedFormMixin, forms.ModelForm):
    """ """

    class Meta:
        model = ImportedArchive
        fields = ('archive', )

    def form_helper(self):
        super().form_helper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'archive'
        )


class ProjectCollaboratorForm(CollaboratorForm):
    """ """

    class Meta(CollaboratorForm.Meta):
        model = ProjectCollaborator
