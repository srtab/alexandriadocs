# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q


class VisibilityQuerySet(models.QuerySet):
    """ """

    def public(self):
        return self.filter(visibility_level=self.model.Level.PUBLIC)

    def private(self):
        return self.filter(visibility_level=self.model.Level.PRIVATE)


class AuthorQuerySet(models.QuerySet):
    """ """

    def author(self, user):
        return self.filter(author=user)


class AuthorVisibilityQueryset(AuthorQuerySet, VisibilityQuerySet):
    """ """

    def visible(self, user=None):
        if user and user.is_authenticated:
            return self.filter(
                Q(visibility_level=self.model.Level.PUBLIC) |
                Q(visibility_level=self.model.Level.PRIVATE, author=user))
        return self.public()
