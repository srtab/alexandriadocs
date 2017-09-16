from django.test import SimpleTestCase
from mock import MagicMock, patch
from projects.models import ImportedArchive, ImportedFile, Project


class ProjectModelTest(SimpleTestCase):

    def setUp(self):
        self.project = Project(title="title", slug="slug")

    def test_str(self):
        self.assertEqual(str(self.project), self.project.title)

    def test_get_absolute_url(self):
        with self.settings(PROJECTS_SERVE_URL="/docs/"):
            self.assertEqual(self.project.get_absolute_url(),
                             "/docs/slug/index.html")

    def test_serve_root_path(self):
        with self.settings(PROJECTS_SERVE_ROOT="/test/"):
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


class ImportedArchiveModelTest(SimpleTestCase):

    def setUp(self):
        self.project = Project(title="title", slug="slug")
        self.archive = ImportedArchive(project=self.project)
        self.archive.archive = MagicMock()

    def test_str(self):
        self.assertEqual(str(self.archive), self.project.title)

    @patch.object(ImportedFile.objects, 'walk')
    @patch('projects.models.tarfile')
    def test_fileify(self, tarfile, walk):
        self.archive.fileify()
        tarfile.open.assert_called_with(self.archive.archive.path, 'r:gz')
        tarfile.open().__enter__().extractall.assert_called_with(
            self.project.serve_root_path)
        walk.assert_called_with(self.project.pk, self.project.serve_root_path)

    def test_post_save(self):
        self.archive.fileify = MagicMock()
        ImportedArchive.post_save(ImportedArchive, self.archive, True)
        self.archive.fileify.assert_called_once()

    def test_post_save_not_created(self):
        self.archive.fileify = MagicMock()
        ImportedArchive.post_save(ImportedArchive, self.archive, False)
        self.archive.fileify.assert_not_called()


class ImportedFileModelTest(SimpleTestCase):

    def setUp(self):
        self.imported_file = ImportedFile(path="/unit/test.html")

    def test_str(self):
        self.assertEqual(str(self.imported_file), "/unit/test.html")

    def test_get_absolute_url(self):
        with self.settings(
                PROJECTS_SERVE_ROOT="/unit/", PROJECTS_SERVE_URL="/docs/"):
            self.assertEqual(self.imported_file.get_absolute_url(),
                             "/docs/test.html")
