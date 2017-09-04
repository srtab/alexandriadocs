# -*- coding: utf-8 -*-
from core.managers import AuthorVisibilityQueryset


class GroupQuerySet(AuthorVisibilityQueryset):
    """ """


GroupManager = GroupQuerySet.as_manager
