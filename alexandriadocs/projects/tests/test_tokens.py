from django.test import SimpleTestCase
from django.utils.crypto import salted_hmac
from mock import Mock
from projects.tokens import token_generator


class ApiTokenGeneratorTest(SimpleTestCase):
    """ """
    def setUp(self):
        self.project = Mock(pk=1, group_id=1)
        self.project2 = Mock(pk=2, group_id=1)

    def test_make_token(self):
        token = token_generator.make_token(self.project)
        expected = salted_hmac(
            token_generator.key_salt,
            token_generator._make_hash_value(self.project),
            secret=token_generator.secret,
        ).hexdigest()
        self.assertEqual(token, expected)

    def test_check_token(self):
        token = token_generator.make_token(self.project)
        self.assertTrue(token_generator.check_token(self.project, token))
        self.assertFalse(token_generator.check_token(self.project2, token))

    def test_check_token_with_empty_args(self):
        self.assertFalse(token_generator.check_token(self.project, None))
        self.assertFalse(token_generator.check_token(None, "token"))

    def test_make_hash_value(self):
        hashv = token_generator._make_hash_value(self.project)
        self.assertEqual(
            hashv, str(self.project.pk) + str(self.project.group_id))
