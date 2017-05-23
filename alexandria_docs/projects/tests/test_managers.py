from __future__ import unicode_literals

from hashlib import md5
from mock import patch

from django.test import TestCase

from projects.models import Project, ImportedFile
from autofixture import create_one


@patch('projects.managers.hashlib.md5', return_value=md5("unit"))
@patch('projects.managers.open')
@patch('projects.managers.os.walk',
       return_value=[("/root/", None, ['index.html', 'main.js'])])
class ImportedFileManagerTest(TestCase):

    def setUp(self):
        self.project = create_one(Project, generate_fk=True)

    def test_walk(self, walk, open, md5):
        """ """
        result = ImportedFile.objects.walk(self.project.pk, "/root/")
        expected = ImportedFile.objects.filter(project_id=self.project.pk)
        self.assertEqual(ImportedFile.objects.count(), 1)
        self.assertQuerysetEqual(result, map(repr, expected))

    def test_walk_with_other_valid_import_extension(self, walk, open, md5):
        """ """
        with self.settings(PROJECTS_VALID_IMPORT_EXTENSION=[".html", ".js"]):
            result = ImportedFile.objects.walk(self.project.pk, "/root/")
        expected = ImportedFile.objects.filter(project_id=self.project.pk)
        self.assertEqual(ImportedFile.objects.count(), 2)
        self.assertQuerysetEqual(result, map(repr, expected), ordered=None)

    def test_walk_delete_previous_imported_files(self, walk, open, md5):
        """ """
        ImportedFile.objects.walk(self.project.pk, "/root/")
        result = ImportedFile.objects.walk(self.project.pk, "/root/")
        expected = ImportedFile.objects.filter(project_id=self.project.pk)
        self.assertEqual(ImportedFile.objects.count(), 1)
        self.assertQuerysetEqual(result, map(repr, expected))
