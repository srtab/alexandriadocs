from __future__ import unicode_literals

from django.test import SimpleTestCase

from projects.models import Project


class ProjectModelTest(SimpleTestCase):

    def test_str(self):
        project = Project(title="title")
        self.assertEqual(str(project), project.title)
