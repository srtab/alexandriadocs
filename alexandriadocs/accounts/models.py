# -*- coding: utf-8 -*-
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class AccessLevel:
    READER = 0
    ADMIN = 1
    OWNER = 2

    choices = (
        (READER, _('Reader')),
        (ADMIN, _('Admin')),
        (OWNER, _('Owner')),
    )
    choices_dist = {
        'READER': READER,
        'ADMIN': ADMIN,
        'OWNER': OWNER
    }


class User(AbstractUser):
    """ """
    slug = AutoSlugField(populate_from='username', unique=True,
                         always_update=True, db_index=True)
    name = models.CharField(_('name'), max_length=128, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("accounts:index", args=[self.slug])


class CollaboratorMixin(models.Model):
    """ """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    access_level = models.PositiveSmallIntegerField(
        _('access level'), choices=AccessLevel.choices,
        default=AccessLevel.READER)

    def __str__(self):
        return "{user} ({level})".format(
            user=self.user, level=self.get_access_level_display())

    class Meta:
        abstract = True
