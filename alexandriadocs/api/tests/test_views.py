from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import post_save
from django.urls import reverse

from model_mommy import mommy
from projects.models import ImportedArchive, Project
from rest_framework import status
from rest_framework.test import APITestCase


mommy.generators.add(
    'autoslug.fields.AutoSlugField', 'model_mommy.random_gen.gen_slug')


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
        post_save.disconnect(ImportedArchive.post_save, sender=ImportedArchive)
        data = {
            'archive': SimpleUploadedFile('docs.tar.gz', b'content')
        }
        response = self.client.post(self.url, data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ImportedArchive.objects.count(), 1)
