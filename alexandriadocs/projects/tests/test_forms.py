from django.test import SimpleTestCase
from projects.forms import ImportedArchiveForm, ProjectEditForm, ProjectForm


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
