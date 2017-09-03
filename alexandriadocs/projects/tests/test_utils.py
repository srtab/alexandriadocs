# -*- coding: utf-8 -*-
from django.test import SimpleTestCase
from projects.models import ImportedArchive, Project
from projects.utils import clean_html, projects_upload_to


class UtilsTest(SimpleTestCase):

    def test_projects_upload_to(self):
        project = Project(slug="title")
        archive = ImportedArchive(project=project)
        result = projects_upload_to(archive, "test.zip")
        self.assertRegexpMatches(result, r"^projects/\d+/\d+/title/test\.zip$")

    def test_clean_html_with_html_content(self):
        result = clean_html("<h1>Title content</h1>")
        self.assertEqual(result, "Title content")

    def test_clean_html_without_html_content(self):
        result = clean_html("Title content")
        self.assertEqual(result, "Title content")

    def test_clean_html_with_special_char(self):
        result = clean_html("Title content¶")
        self.assertEqual(result, "Title content")
