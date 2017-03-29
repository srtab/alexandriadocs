from __future__ import unicode_literals

from django.test import SimpleTestCase
from django.urls import reverse


class UploadProjectArchiveViewTest(SimpleTestCase):

    def setUp(self):
        self.url = reverse('api:project-archive-upload', args=['v1'])

    def test_post_with_unauthenticated_user(self):
        """must be athenticated to access api"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)
