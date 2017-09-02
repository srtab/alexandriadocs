# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel


@python_2_unicode_compatible
class Group(TimeStampedModel):
    """House several projects under the same namespace.
    """
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='name')

    class Meta:
        verbose_name = _('group')

    def __str__(self):
        return self.name
