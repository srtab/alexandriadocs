# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class VisibilityMixin(models.Model):
    """Defines visibility of model """

    class Level:
        PRIVATE = 0
        PUBLIC = 1

        choices = (
            (PRIVATE, _('Private')),
            (PUBLIC, _('Public')),
        )

    visibility_level = models.PositiveSmallIntegerField(
        _('visibility level'), choices=Level.choices, default=Level.PRIVATE)

    class Meta:
        abstract = True

    @property
    def is_private(self):
        return self.visibility_level == self.Level.PRIVATE

    @property
    def is_public(self):
        return self.visibility_level == self.Level.PUBLIC
