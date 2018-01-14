from unittest.mock import Mock

from django.test import SimpleTestCase

from search.templatetags.search_tags import extract_objects


class ProjectModelTest(SimpleTestCase):

    def setUp(self):
        self.result_list = [
            Mock(object=1),
            Mock(object=2),
        ]

    def test_extract_objects(self):
        result = extract_objects(self.result_list)
        self.assertEqual(result, [
            (self.result_list[0], self.result_list[0].object),
            (self.result_list[1], self.result_list[1].object)
        ])

    def test_extract_objects_only_objects(self):
        result = extract_objects(self.result_list, method='only_objects')
        self.assertEqual(result, [
            self.result_list[0].object,
            self.result_list[1].object
        ])
