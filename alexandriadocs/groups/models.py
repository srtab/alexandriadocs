# -*- coding: utf-8 -*-
from core.models import VisibilityMixin
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import (
    TimeStampedModel, TitleSlugDescriptionModel)


class Group(VisibilityMixin, TitleSlugDescriptionModel, TimeStampedModel):
    """House several projects under the same namespace.
    """

    class Meta:
        verbose_name = _('group')

    def __str__(self):
        return self.title
