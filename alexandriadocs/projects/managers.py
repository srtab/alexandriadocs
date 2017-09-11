import hashlib
import os

from core.managers import AuthorVisibilityQuerySet
from django.conf import settings
from django.db import models
from django.db.models import Q


class ProjectQuerySet(AuthorVisibilityQuerySet):
    """ """

    def visible(self, user=None):
        """
        Unauthenticated user can only view public projects in public groups.
        Authenticated user can see public projects in public groups or private
        projects in private/public groups if it is the author of both.
        TODO: check if query is heavy
        """
        if user and user.is_authenticated:
            return self.filter(
                Q(visibility_level=self.model.Level.PUBLIC) |
                Q(visibility_level=self.model.Level.PRIVATE, author=user),
                Q(group__visibility_level=self.model.Level.PUBLIC) |
                Q(group__visibility_level=self.model.Level.PRIVATE,
                  author=user))
        return self.filter(visibility_level=self.model.Level.PUBLIC,
                           group__visibility_level=self.model.Level.PUBLIC)

ProjectManager = ProjectQuerySet.as_manager


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
