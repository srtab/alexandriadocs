# -*- coding: utf-8 -*-
from accounts.forms import CollaboratorForm
from core.forms import UntaggedFormMixin
from crispy_forms.layout import Div, Layout
from django import forms
from groups.models import Group, GroupCollaborator


GROUP_COMMON_FIELDS = ('title', 'description')


class GroupForm(UntaggedFormMixin, forms.ModelForm):
    """ """

    class Meta:
        model = Group
        fields = GROUP_COMMON_FIELDS + ('visibility_level',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'visibility_level': forms.RadioSelect
        }


class GroupEditForm(GroupForm):
    """ """

    class Meta(GroupForm.Meta):
        fields = GROUP_COMMON_FIELDS
        widgets = {
            'description': GroupForm.Meta.widgets['description'],
        }


class GroupVisibilityForm(UntaggedFormMixin, forms.ModelForm):
    """ """
    class Meta:
        model = Group
        fields = ('visibility_level',)
        widgets = {
            'visibility_level': GroupForm.Meta.widgets['visibility_level']
        }

    def form_helper(self):
        super().form_helper()
        self.helper.form_show_labels = False


class GroupCollaboratorForm(CollaboratorForm):
    """ """

    class Meta(CollaboratorForm.Meta):
        model = GroupCollaborator

    def form_helper(self):
        super().form_helper()
        self.helper.layout = Layout(
            Div(
                Div('user', css_class="col-md-6"),
                Div('access_level', css_class="col-md-6"),
                css_class="row",
            ),
        )
