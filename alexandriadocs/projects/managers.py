import hashlib
import os

from django.conf import settings
from django.db import models
from django.db.models import Q


class ProjectQuerySet(models.QuerySet):
    """ """

    def public(self):
        return self.filter(visibility_level=self.model.Level.PUBLIC,
                           group__visibility_level=self.model.Level.PUBLIC)

    def collaborate(self, user=None):
        if user and user.is_authenticated:
            group_ids = user.collaborate_groups.values('pk')
            project_ids = user.collaborate_projects.values('pk')
            return self.filter(Q(pk__in=project_ids) | Q(group__in=group_ids))
        return self.empty()

    def public_or_collaborate(self, user=None):
        if user and user.is_authenticated:
            group_ids = user.collaborate_groups.values('pk')
            project_ids = user.collaborate_projects.values('pk')
            return self.filter(
                Q(pk__in=project_ids) | Q(group__in=group_ids) |
                Q(visibility_level=self.model.Level.PUBLIC,
                  group__visibility_level=self.model.Level.PUBLIC))
        return self.public()


ProjectManager = ProjectQuerySet.as_manager


class ImportedFileManager(models.Manager):
    """ """

    def walk(self, project_id, walkpath):
        """Walk through waklpath, create an object for every valid file found.
        All objects associated to the project previously created will be
        deleted."""
        import_files = []
        # walk through extracted files
        for root, __, filenames in os.walk(walkpath):
            for filename in filenames:
                extension = os.path.splitext(filename)[-1].lower()
                if extension in settings.PROJECTS_VALID_IMPORT_EXTENSION:
                    full_path = os.path.abspath(os.path.join(root, filename))
                    with open(full_path, 'rb') as fp:
                        md5 = hashlib.md5(fp.read()).hexdigest()
                    obj, created = self.get_or_create(
                        project_id=project_id,
                        path=full_path,
                        md5=md5
                    )
                    import_files.append(obj)
        # delete all previous imported files to avoid indexing old data
        imported_ids = [ifile.pk for ifile in import_files]
        self.filter(project_id=project_id).exclude(pk__in=imported_ids)\
            .delete()
        return import_files
