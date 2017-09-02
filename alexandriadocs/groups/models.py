# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import (
    TimeStampedModel, TitleSlugDescriptionModel)


class Group(TitleSlugDescriptionModel, TimeStampedModel):
    """House several projects under the same namespace.
    """

    class Meta:
        verbose_name = _('group')

    def __str__(self):
        return self.title
