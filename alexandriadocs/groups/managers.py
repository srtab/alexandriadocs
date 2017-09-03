# -*- coding: utf-8 -*-
from core.managers import VisibilityQuerySet
from django.db.models import Q


class GroupQuerySet(VisibilityQuerySet):

    def visible(self, user=None):
        if user and user.is_authenticated:
            return self.filter(
                Q(visibility_level=self.model.Level.PUBLIC) |
                Q(visibility_level=self.model.Level.PRIVATE, author=user))
        return self.public()


GroupManager = GroupQuerySet.as_manager
