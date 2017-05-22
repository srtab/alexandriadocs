# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import skip
from mock import patch

from django.test import SimpleTestCase

from projects.search_indexes import ProjectIndex, ImportedFileIndex
from projects.models import Project, ImportedFile


class ProjectIndexTest(SimpleTestCase):
    """ """

    def setUp(self):
        """ """
        self.project_index = ProjectIndex()

    def test_get_model(self):
        """ """
        self.assertEqual(self.project_index.get_model(), Project)

    @patch.object(Project, 'get_absolute_url', return_value="/docs/index.html")
    def test_prepare_absolute_url(self, get_absolute_url):
        """ """
        project = Project()
        result = self.project_index.prepare_absolute_url(project)
        self.assertEqual(result, "/docs/index.html")


class ImportedFileIndexTest(SimpleTestCase):
    """ """

    def setUp(self):
        """ """
        self.imported_file_index = ImportedFileIndex()

    def test_get_model(self):
        """ """
        self.assertEqual(self.imported_file_index.get_model(), ImportedFile)

    @patch.object(ImportedFile, 'get_absolute_url', return_value="/test.html")
    def test_prepare_absolute_url(self, get_absolute_url):
        """ """
        imported_file = ImportedFile()
        result = self.imported_file_index.prepare_absolute_url(imported_file)
        self.assertEqual(result, "/test.html")

    @skip("TODO")
    def test_prepare(self):
        """ """
