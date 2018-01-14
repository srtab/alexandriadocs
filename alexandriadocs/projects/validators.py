from zipfile import ZipFile

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

import magic


@deconstructible
class MimeTypeValidator(object):
    """Validator for files, checking the mimetype."""

    mime_message = _(
        "MIME type '%(mimetype)s' is not valid. "
        "Allowed types are: %(allowed_mimetypes)s."
    )

    def __init__(self, allowed_mimetypes=None, message=None):
        self.allowed_mimetypes = allowed_mimetypes
        if message is not None:
            self.mime_message = message

    def __call__(self, value):
        # Check the content type
        mimetype = magic.from_buffer(value.read(1024), mime=True)
        if self.allowed_mimetypes and mimetype not in self.allowed_mimetypes:
            message = self.mime_message % {
                'mimetype': mimetype,
                'allowed_mimetypes': ', '.join(self.allowed_mimetypes)
            }
            raise ValidationError(message)


@deconstructible
class StructureValidator(object):
    """Validates archives structures."""

    message = _(
        "The archive structure is not as expected. Must contain at least an "
        "index.html as root element."
    )

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def __call__(self, value):
        with ZipFile(value) as myzip:
            if myzip.testzip():
                raise ValidationError(_("Invalid zip file provided."))
            try:
                myzip.getinfo("index.html")
            except KeyError:
                raise ValidationError(self.message)
