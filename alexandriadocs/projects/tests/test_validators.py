import io

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from mock import patch
from projects.validators import MimeTypeValidator


class MimeTypeValidatorTest(SimpleTestCase):
    """ """

    def setUp(self):
        self.archive = io.StringIO("test unit")

    @patch('projects.validators.magic')
    def test_empty_allowed_mimetype(self, magic):
        """ """
        validator = MimeTypeValidator()
        validator(self.archive)
        magic.from_buffer.assert_called_with("test unit", mime=True)

    @patch('projects.validators.magic')
    def test_with_valid_mymetype(self, magic):
        magic.from_buffer.return_value = "mimetype"
        validator = MimeTypeValidator(allowed_mimetypes=["mimetype"])
        returned = validator(self.archive)
        self.assertIsNone(returned)

    @patch('projects.validators.magic')
    def test_with_invalid_mymetype(self, magic):
        magic.from_buffer.return_value = "invalid_mimetype"
        validator = MimeTypeValidator(allowed_mimetypes=["mimetype"])
        expected_msg = (
            "MIME type 'invalid_mimetype' is not valid. "
            "Allowed types are: mimetype."
        )
        with self.assertRaisesRegex(ValidationError, expected_msg):
            validator(self.archive)

    @patch('projects.validators.magic')
    def test_with_invalid_mymetype_and_custom_message(self, magic):
        magic.from_buffer.return_value = "invalid_mimetype"
        validator = MimeTypeValidator(
            allowed_mimetypes=["mimetype"], message="Invalid mimetype")
        with self.assertRaisesRegex(ValidationError, "Invalid mimetype"):
            validator(self.archive)
