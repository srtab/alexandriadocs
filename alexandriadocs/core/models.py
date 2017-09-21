# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField


class TitleSlugDescriptionMixin(models.Model):
    """
    An abstract base class model that provides title and description fields
    and a self-managed "slug" field that populates from the title.
    """
    title = models.CharField(_('title'), max_length=128)
    slug = AutoSlugField(_('slug'), populate_from='title')
    description = models.CharField(
        _('description'), max_length=256, blank=True, null=True)

    class Meta:
        abstract = True


class VisibilityMixin(models.Model):
    """
    An abstract base class models that provied visibility_level field.
    """

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
