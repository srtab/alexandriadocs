# -*- coding: utf-8 -*-
from core.managers import AuthorVisibilityQuerySet


class GroupQuerySet(AuthorVisibilityQuerySet):
    """ """


GroupManager = GroupQuerySet.as_manager
