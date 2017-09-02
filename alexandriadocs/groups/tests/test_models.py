from __future__ import unicode_literals

from django.test import SimpleTestCase
from groups.models import Group


class GroupModelTest(SimpleTestCase):

    def test_str(self):
        group = Group(name="name")
        self.assertEqual(str(group), group.name)
