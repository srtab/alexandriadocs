# -*- coding: utf-8 -*-
from hashlib import md5
from unittest.mock import Mock, mock_open, patch

from autofixture import create_one
from django.test import SimpleTestCase, TestCase
from projects.managers import ProjectQuerySet
from projects.models import ImportedFile, Project


class ProjectQuerySetTest(SimpleTestCase):

    def setUp(self):
        self.queryset = ProjectQuerySet(model=Project)

    @patch.object(ProjectQuerySet, 'filter')
    def test_public(self, mfilter):
        self.queryset.public()
        mfilter.assert_called_with(
            visibility_level=Project.Level.PUBLIC,
            group__visibility_level=Project.Level.PUBLIC)

    def test_collaborate_user_none(self):
        result = self.queryset.collaborate()
        self.assertEqual(str(result), str(self.queryset.none()))

    @patch.object(ProjectQuerySet, 'filter')
    def test_collaborate_user_authenticated(self, mfilter):
        user = Mock(is_authenticated=True)
        self.queryset.collaborate(user=user)
        user.collaborate_groups.values.assert_called_with('pk')
        user.collaborate_projects.values.assert_called_with('pk')
        mfilter.assert_called_once()

    @patch.object(ProjectQuerySet, 'public')
    def test_public_or_collaborate_user_none(self, mpublic):
        self.queryset.public_or_collaborate()
        mpublic.assert_called_with()

    @patch.object(ProjectQuerySet, 'filter')
    def test_public_or_collaborate_user_authenticated(self, mfilter):
        user = Mock(is_authenticated=True)
        self.queryset.public_or_collaborate(user=user)
        user.collaborate_groups.values.assert_called_with('pk')
        user.collaborate_projects.values.assert_called_with('pk')
        mfilter.assert_called_once()


@patch('projects.managers.hashlib.md5', return_value=md5(b"unit"))
@patch('projects.managers.open', mock_open(), create=True)
@patch('projects.managers.os.walk',
       return_value=[("/root/", None, ['index.html', 'main.js'])])
class ImportedFileManagerTest(TestCase):

    def setUp(self):
        self.project = create_one(Project, generate_fk=True)

    def test_walk(self, walk, md5):
        """ """
        result = ImportedFile.objects.walk(self.project.pk, "/root/")
        expected = ImportedFile.objects.filter(project_id=self.project.pk)
        self.assertEqual(ImportedFile.objects.count(), 1)
        self.assertQuerysetEqual(result, map(repr, expected))

    def test_walk_with_other_valid_import_extension(self, walk, md5):
        """ """
        with self.settings(PROJECTS_VALID_IMPORT_EXTENSION=[".html", ".js"]):
            result = ImportedFile.objects.walk(self.project.pk, "/root/")
        expected = ImportedFile.objects.filter(project_id=self.project.pk)
        self.assertEqual(ImportedFile.objects.count(), 2)
        self.assertQuerysetEqual(result, map(repr, expected), ordered=None)

    def test_walk_delete_previous_imported_files(self, walk, md5):
        """ """
        ImportedFile.objects.walk(self.project.pk, "/root/")
        result = ImportedFile.objects.walk(self.project.pk, "/root/")
        expected = ImportedFile.objects.filter(project_id=self.project.pk)
        self.assertEqual(ImportedFile.objects.count(), 1)
        self.assertQuerysetEqual(result, map(repr, expected))
