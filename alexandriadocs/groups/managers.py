# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q


class GroupQuerySet(models.QuerySet):
    """ """
    def public(self):
        return self.filter(visibility_level=self.model.Level.PUBLIC)

    def public_and_collaborate(self, user=None):
        if user and user.is_authenticated:
            group_ids = user.collaborate_groups.values('pk')
            return self.filter(
                Q(pk__in=group_ids) |
                Q(visibility_level=self.model.Level.PUBLIC))
        return self.public()


GroupManager = GroupQuerySet.as_manager
