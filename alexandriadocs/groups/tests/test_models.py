from django.test import SimpleTestCase
from groups.models import Group


class GroupModelTest(SimpleTestCase):

    def test_str(self):
        group = Group(title="title")
        self.assertEqual(str(group), group.title)
