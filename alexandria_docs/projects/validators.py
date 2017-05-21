from __future__ import unicode_literals

# import tarfile
import magic
import os

from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


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
class IntegrityTarValidator(object):
    """ """

    message = _("Unsafe filenames on tar.")

    def __init__(self, target_dir, message=None):
        """ """
        self.target_dir = os.path.abspath(target_dir)
        if message is not None:
            self.message = message

    def __call__(self, value):
        """TODO: cant open tarfile if value is a InMemoryUploadedFile"""
        # with tarfile.open(fileobj=fileobj) as tar:
        #     for filename in tar.getnames():
        #         fullpath = os.path.join(self.target_dir, filename)
        #         if not os.path.abspath(fullpath) == fullpath:
        #             raise ValidationError(self.message)
