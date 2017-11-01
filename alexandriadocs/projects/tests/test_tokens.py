from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36

from projects.tokens import token_generator


class ApiTokenGeneratorTest(SimpleTestCase):
    """ """
    def setUp(self):
        self.project = Mock(pk=1, group_id=1, author_id=2)
        self.project2 = Mock(pk=2, group_id=1, author_id=2)

    def test_make_token(self):
        token = token_generator.make_token(self.project)
        id_b36 = int_to_base36(self.project.pk)
        expected = salted_hmac(
            token_generator.key_salt,
            token_generator._make_hash_value(self.project),
            secret=token_generator.secret,
        ).hexdigest()
        self.assertEqual(token, '-'.join([id_b36, expected]))

    @patch.object(token_generator, 'get_project')
    def test_check_token(self, mget_project):
        mget_project.return_value = self.project
        token = token_generator.make_token(self.project)
        token2 = token_generator.make_token(self.project2)
        self.assertTrue(token_generator.check_token(token))
        self.assertFalse(token_generator.check_token(token2))

    def test_check_token_with_empty_args(self):
        self.assertFalse(token_generator.check_token(None))

    def test_make_hash_value(self):
        hashv = token_generator._make_hash_value(self.project)
        self.assertEqual(hashv, "121")

    @patch.object(token_generator, 'get_project_id', return_value=None)
    def test_get_object_invalid_valid(self, mproject_id):
        self.assertIsNone(token_generator.get_project('invalid'))
        mproject_id.assert_called_with('invalid')

    @patch('projects.tokens.apps.get_model', return_value=Mock())
    @patch.object(token_generator, 'get_project_id', return_value=1)
    def test_get_object_valid_token(self, mproject_id, model):
        self.assertIsNotNone(token_generator.get_project('valid'))
        model().objects.filter.assert_called_with(pk=1)
        model().objects.filter().first.assert_called_with()

    def test_get_object_id_invalid_token(self):
        self.assertIsNone(token_generator.get_project_id('invalid'))

    def test_get_object_id_valid_token(self):
        self.assertEqual(token_generator.get_project_id('1-valid'), 1)
