from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import force_authenticate, APIRequestFactory

from projects.models import Project, ProjectArchive, Organization
from api.views import UploadProjectArchiveView


class UploadProjectArchiveViewTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UploadProjectArchiveView.as_view()
        self.user = get_user_model().objects.create_user(
            username='test',
            email='t@t.c',
            password='pass'
        )
        self.project = Project.objects.create(
            author=self.user,
            organization=Organization.objects.create()
        )

    def test_post_with_unauthenticated_user(self):
        """must be athenticated to access api"""
        request = self.factory.post('/test/', {})
        response = self.view(request).render()
        self.assertEqual(response.status_code, 401)

    def test_post_with_authenticated_user(self):
        """"""
        # to avoid files extraction
        post_save.disconnect(ProjectArchive.post_save, sender=ProjectArchive)
        data = {
            'project': self.project.pk,
            'archive': open('api/tests/test.tar.gz')
        }
        request = self.factory.post('/test/', data)
        force_authenticate(request, user=self.user)
        response = self.view(request).render()
        self.assertEqual(response.status_code, 201)
