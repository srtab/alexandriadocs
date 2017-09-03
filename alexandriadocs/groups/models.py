# -*- coding: utf-8 -*-
from core.models import TitleSlugDescriptionMixin, VisibilityMixin
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from groups.managers import GroupManager


class Group(VisibilityMixin, TitleSlugDescriptionMixin, TimeStampedModel):
    """House several projects under the same namespace, just like a folder
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT)
    objects = GroupManager()

    class Meta:
        ordering = ['title', 'created']
        verbose_name = _('group')

    def __str__(self):
        return self.title
