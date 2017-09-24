# -*- coding: utf-8 -*-
from unittest.mock import patch

from accounts.models import AccessLevel
from django.forms import ValidationError
from django.test import SimpleTestCase
from projects.forms import (
    ImportedArchiveForm, ProjectEditForm, ProjectForm, ProjectVisibilityForm)


class ProjectFormTest(SimpleTestCase):
    """ """
    def setUp(self):
        self.form = ProjectForm()

    def test_init(self):
        self.assertEqual(self.form.fields['title'].label, 'Project name')
        self.assertEqual(self.form.fields['repo'].widget.attrs['placeholder'],
                         'ex: https://github.com/srtab/alexandriadocs')
        self.assertEqual(self.form.fields['tags'].widget.attrs['placeholder'],
                         'ex: django, python')

    def test_form_helper(self):
        self.assertIsNotNone(self.form.helper.layout)

    @patch('projects.forms.group_access_checker.has_access',
           return_value=False)
    def test_clean_group_without_access(self, mhas_access):
        setattr(self.form, 'cleaned_data', {})
        with self.assertRaises(ValidationError):
            self.form.clean_group()
            mhas_access.assert_called_with(None, None, AccessLevel.ADMIN)

    @patch('projects.forms.group_access_checker.has_access', return_value=True)
    def test_clean_group_with_access(self, mhas_access):
        setattr(self.form, 'cleaned_data', {'group': 'group'})
        self.assertEqual(self.form.clean_group(), 'group')


class ProjectEditFormTest(SimpleTestCase):

    def test_form_helper(self):
        form = ProjectEditForm()
        self.assertIsNotNone(form.helper.layout)
        self.assertEqual(form.helper.layout[0], 'title')


class ImportedArchiveFormTest(SimpleTestCase):

    def test_form_helper(self):
        form = ImportedArchiveForm()
        self.assertIsNotNone(form.helper.layout)
        self.assertEqual(form.helper.layout[0], 'archive')


class ProjectVisibilityFormTest(SimpleTestCase):

    def test_form_helper(self):
        form = ProjectVisibilityForm()
        self.assertFalse(form.helper.form_show_labels)
