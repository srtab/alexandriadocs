from unittest.mock import MagicMock, PropertyMock, patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.urls import reverse

from accounts.models import AccessLevel
from groups.models import Group
from projects.models import (
    ImportedArchive, ImportedFile, Project, ProjectCollaborator
)


class ProjectModelTest(SimpleTestCase):

    def setUp(self):
        self.project = Project(name="name", slug="slug")

    def test_str(self):
        self.assertEqual(str(self.project), self.project.name)

    def test_fullname(self):
        self.project.group = Group(name="Group")
        self.assertEqual("Group / name", self.project.fullname)

    @patch.object(Group, 'is_private', new_callable=PropertyMock,
                  return_value=True)
    def test_is_private_with_group_private(self, mis_private):
        self.project.group = Group()
        self.project.visibility_level = Project.Level.PRIVATE
        self.assertTrue(self.project.is_private)
        self.project.visibility_level = Project.Level.PUBLIC
        self.assertTrue(self.project.is_private)

    @patch.object(Group, 'is_private', new_callable=PropertyMock,
                  return_value=False)
    def test_is_private_with_group_public(self, mis_private):
        self.project.group = Group()
        self.project.visibility_level = Project.Level.PRIVATE
        self.assertTrue(self.project.is_private)
        self.project.visibility_level = Project.Level.PUBLIC
        self.assertFalse(self.project.is_private)

    @patch.object(Group, 'is_public', new_callable=PropertyMock,
                  return_value=True)
    def test_is_public_with_group_public(self, mis_public):
        self.project.group = Group()
        self.project.visibility_level = Project.Level.PRIVATE
        self.assertTrue(self.project.is_public)
        self.project.visibility_level = Project.Level.PUBLIC
        self.assertTrue(self.project.is_public)

    @patch.object(Group, 'is_public', new_callable=PropertyMock,
                  return_value=False)
    def test_is_public_with_group_private(self, mis_public):
        self.project.group = Group()
        self.project.visibility_level = Project.Level.PRIVATE
        self.assertFalse(self.project.is_public)
        self.project.visibility_level = Project.Level.PUBLIC
        self.assertTrue(self.project.is_public)

    def test_get_absolute_url(self):
        expected = reverse('projects:project-detail', args=["slug"])
        self.assertEqual(self.project.get_absolute_url(), expected)

    def test_get_docs_url(self):
        expected = reverse('serve-docs', args=["slug", "index.html"])
        with self.settings(SENDFILE_URL="/docs/"):
            self.assertEqual(self.project.get_docs_url(), expected)

    def test_serve_root_path(self):
        with self.settings(SENDFILE_ROOT="/test/"):
            self.assertEqual(self.project.serve_root_path, "/test/slug")

    @patch.object(Project, 'imported_archives')
    def test_last_imported_archive_date(self, mimported_archives):
        mimported_archives.latest().created = 'created'
        result = self.project.last_imported_archive_date
        mimported_archives.latest.assert_called_with('created')
        self.assertEqual(result, 'created')

    @patch.object(Project, 'imported_archives')
    def test_last_imported_archive_date_empty(self, mimported_archives):
        mimported_archives.latest.side_effect = ImportedArchive.DoesNotExist
        result = self.project.last_imported_archive_date
        self.assertIsNone(result)

    @patch.object(Project, 'imported_archives')
    def test_imported_archive_exists(self, mimported_archives):
        self.project.imported_archive_exists
        mimported_archives.exists.assert_called_with()

    @patch.object(Project, 'imported_files')
    def test_imported_files_count(self, mimported_files):
        self.project.imported_files_count
        mimported_files.count.assert_called_with()

    @patch('projects.models.token_generator.make_token', return_value="token")
    def test_api_token(self, mmake_token):
        self.assertEqual(self.project.api_token, 'token')
        mmake_token.assert_called_with(self.project)

    @patch.object(Project, 'objects')
    def test_clean(self, mobjects):
        mobjects.filter().exclude().exists.return_value = False
        Project(pk=1, name="name", group_id=10).clean()
        mobjects.filter.assert_called_with(group_id=10, name__iexact='name')
        mobjects.filter().exclude.assert_called_with(id=1)

    @patch.object(Project, 'objects')
    def test_clean_invalid(self, mobjects):
        mobjects.filter().exclude().exists.return_value = True
        with self.assertRaises(ValidationError):
            Project(pk=1, name="name", group_id=10).clean()

    @patch.object(ProjectCollaborator, 'objects')
    def test_post_save_with_created_true(self, mobjects):
        Project.post_save(Project, Project(pk=1, author_id=1), True)
        mobjects.create.assert_called_with(
            project_id=1, user_id=1, access_level=AccessLevel.OWNER)

    @patch.object(ProjectCollaborator, 'objects')
    def test_post_save_with_created_false(self, mobjects):
        Project.post_save(Project, None, False)
        mobjects.create.assert_not_called()


class ImportedArchiveModelTest(SimpleTestCase):

    def setUp(self):
        self.project = Project(name="name", slug="slug")
        self.archive = ImportedArchive(project=self.project)
        self.archive.archive = MagicMock()

    def test_str(self):
        self.assertEqual(str(self.archive), self.project.name)

    @patch.object(ImportedFile.objects, 'walk')
    @patch('projects.models.ZipFile')
    def test_filesify(self, zipfile, walk):
        self.archive.filesify()
        zipfile.assert_called_with(self.archive.archive.path)
        zipfile().__enter__().extractall.assert_called_with(
            self.project.serve_root_path)
        walk.assert_called_with(self.project.pk, self.project.serve_root_path)

    def test_post_save(self):
        self.archive.filesify = MagicMock()
        ImportedArchive.post_save(ImportedArchive, self.archive, True)
        self.assertTrue(self.archive.filesify.called)

    def test_post_save_not_created(self):
        self.archive.filesify = MagicMock()
        ImportedArchive.post_save(ImportedArchive, self.archive, False)
        self.archive.filesify.assert_not_called()


class ImportedFileModelTest(SimpleTestCase):

    def setUp(self):
        self.imported_file = ImportedFile(
            path="/protected/unit/test.html", project=Project(slug='slug'))

    def test_str(self):
        self.assertEqual(str(self.imported_file), "/protected/unit/test.html")

    def test_get_absolute_url(self):
        with self.settings(SENDFILE_ROOT="/protected/"):
            self.assertEqual(self.imported_file.get_absolute_url(),
                             "/docs/slug/test.html")
