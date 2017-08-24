# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.test import SimpleTestCase
from mock import Mock, patch
from projects.models import ImportedFile, Project
from projects.search_indexes import ImportedFileIndex, ProjectIndex


class ProjectIndexTest(SimpleTestCase):
    """ """

    def setUp(self):
        """ """
        self.project_index = ProjectIndex()

    def test_get_model(self):
        """ """
        self.assertEqual(self.project_index.get_model(), Project)

    @patch.object(Project, 'get_absolute_url', return_value="/docs/index.html")
    def test_prepare_absolute_url(self, mget_absolute_url):
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
    def test_prepare_absolute_url(self, mget_absolute_url):
        """ """
        imported_file = ImportedFile()
        result = self.imported_file_index.prepare_absolute_url(imported_file)
        self.assertEqual(result, "/test.html")

    @patch.object(ImportedFileIndex, 'get_file_content')
    @patch("projects.search_indexes.HtmlExtractor")
    def test_prepare(self, extractor_class, mget_file_content):
        """ """
        extractor_class.return_value = Mock(title="Title", content="Content")
        returned = self.imported_file_index.prepare(Mock())
        extractor_class.assert_called_with(mget_file_content())
        self.assertIn('title', returned)
        self.assertIn('body', returned)
        self.assertIn('text', returned)
        self.assertEqual(returned['title'], "Title")
        self.assertEqual(returned['body'], "Content")
        self.assertIn("Content", returned['text'])

    @patch("projects.search_indexes.codecs.open")
    def test_get_file_content(self, mopen):
        """ """
        obj = Mock()
        self.imported_file_index.get_file_content(obj)
        mopen.assert_called_with(obj.path, encoding='utf-8', mode='rb')

    @patch("projects.search_indexes.codecs.open", side_effect=IOError())
    def test_get_file_content_file_doesnt_exist(self, mopen):
        """ """
        result = self.imported_file_index.get_file_content(Mock())
        self.assertIsNone(result)
