from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from model_mommy import mommy
from projects.models import ImportedArchive, ImportedFile, Project
from rest_framework import status
from rest_framework.test import APITestCase

mommy.generators.add(
    'autoslug.fields.AutoSlugField', 'model_mommy.random_gen.gen_slug')


VALID_ZIP_FILE = (
    b'PK\x03\x04\x14\x00\x08\x00\x08\x00\x05\x06\x8bJ\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\n\x00 \x00index.htmlUT\r\x00\x07\xbb\x19\xecX'
    b'\x1a\xc3ZZ\x1a\xc3ZZux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00'
    b'\x00\x03\x00PK\x07\x08\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00'
    b'PK\x01\x02\x14\x03\x14\x00\x08\x00\x08\x00\x05\x06\x8bJ\x00\x00\x00\x00'
    b'\x02\x00\x00\x00\x00\x00\x00\x00\n\x00 \x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\xb4\x81\x00\x00\x00\x00index.htmlUT\r\x00\x07\xbb\x19\xecX\x1a\xc3'
    b'ZZ\x1a\xc3ZZux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05'
    b'\x06\x00\x00\x00\x00\x01\x00\x01\x00X\x00\x00\x00Z\x00\x00\x00\x00\x00'
)


class ImportedArchiveViewTest(APITestCase):

    def setUp(self):
        self.project = mommy.make(Project)
        self.headers = {'HTTP_API_KEY': self.project.api_token}
        self.url = reverse('api:project-imported-archive', args=['v1'])

    def test_post_without_api_token(self):
        """must be athenticated to access api"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('projects.models.MimeTypeValidator.__call__', return_value=None)
    def test_post(self, mmime):
        # to avoid files extraction
        data = {
            'archive': SimpleUploadedFile('test.zip', VALID_ZIP_FILE)
        }
        response = self.client.post(self.url, data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ImportedArchive.objects.count(), 1)
        self.assertEqual(ImportedFile.objects.count(), 1)
