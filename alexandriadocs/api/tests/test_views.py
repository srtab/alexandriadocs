from api.views import ImportArchiveView
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from groups.models import Group
from projects.models import ImportedArchive, Project
from rest_framework.test import APIRequestFactory, force_authenticate


class ImportedArchiveViewTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ImportArchiveView.as_view()
        self.user = get_user_model().objects.create_user(
            username='test',
            email='t@t.c',
            password='pass'
        )
        self.project = Project.objects.create(
            author=self.user,
            group=Group.objects.create(author=self.user,)
        )

    def test_post_with_unauthenticated_user(self):
        """must be athenticated to access api"""
        request = self.factory.post('/test/', {})
        response = self.view(request).render()
        self.assertEqual(response.status_code, 401)

    def test_post_with_authenticated_user(self):
        """"""
        # to avoid files extraction
        post_save.disconnect(ImportedArchive.post_save, sender=ImportedArchive)
        data = {
            'project': self.project.pk,
            'archive': open('api/tests/test.tar.gz', 'rb')
        }
        request = self.factory.post('/test/', data)
        force_authenticate(request, user=self.user)
        response = self.view(request).render()
        self.assertEqual(response.status_code, 201)
