from django.db import models

from accounts.models import AccessLevel


class CollaboratorQuerySet(models.QuerySet):
    """ """
    MIN_OWNER = 1

    def can_delete(self):
        return self.filter(access_level=AccessLevel.OWNER).count() > \
            self.MIN_OWNER


CollaboratorManager = CollaboratorQuerySet.as_manager
