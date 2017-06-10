from __future__ import unicode_literals

import hashlib
import os

from django.conf import settings
from django.db import models


class ImportedFileManager(models.Manager):
    """ """

    def walk(self, project_id, walkpath):
        """Walk through waklpath, create an object for every valid file found.
        All objects associated to the project previously created will be
        deleted."""
        import_files = []
        # delete all previous imported files to avoid indexing old data
        self.filter(project_id=project_id).delete()
        # walk through extratect files
        for root, __, filenames in os.walk(walkpath):
            for filename in filenames:
                extension = os.path.splitext(filename)[-1].lower()
                if extension in settings.PROJECTS_VALID_IMPORT_EXTENSION:
                    full_path = os.path.abspath(os.path.join(root, filename))
                    with open(full_path, 'rb') as fp:
                        md5 = hashlib.md5(fp.read()).hexdigest()
                    import_files.append(self.model(
                        project_id=project_id,
                        path=full_path,
                        md5=md5
                    ))
        self.bulk_create(import_files)
        return self.filter(project_id=project_id)
