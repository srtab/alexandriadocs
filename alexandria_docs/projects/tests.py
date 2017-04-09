from __future__ import unicode_literals

from django.test import SimpleTestCase

from projects.models import Organization, Project, ProjectArchive
from projects.utils import projects_upload_to


class OrganizationModelTest(SimpleTestCase):

    def test_str(self):
        organization = Organization(name="name")
        self.assertEqual(str(organization), organization.name)


class ProjectModelTest(SimpleTestCase):

    def test_str(self):
        project = Project(title="title")
        self.assertEqual(str(project), project.title)


class ProjectArchiveModelTest(SimpleTestCase):

    def test_str(self):
        project = Project(title="title")
        archive = ProjectArchive(project=project)
        self.assertEqual(str(archive), project.title)


class UtilsTest(SimpleTestCase):

    def test_projects_upload_to(self):
        project = Project(slug="title")
        archive = ProjectArchive(project=project)
        result = projects_upload_to(archive, "test.zip")
        self.assertRegexpMatches(result, r"^projects/\d+/\d+/title/test\.zip$")
