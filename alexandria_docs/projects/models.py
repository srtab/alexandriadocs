from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import models

from django_extensions.db.models import (
    TitleSlugDescriptionModel, TimeStampedModel)


@python_2_unicode_compatible
class Project(TitleSlugDescriptionModel, TimeStampedModel):
    """ """

    class Kind:
        PROJECT = 0
        SUBPROJECT = 0

        choices = (
            (PROJECT, _('project')),
            (SUBPROJECT, _('sub-project'))
        )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('uploaded by'))
    kind = models.PositiveSmallIntegerField(
        _('kind'), choices=Kind.choices, default=Kind.PROJECT)

    class Meta:
        verbose_name = _('project')

    def __str__(self):
        return self.title
