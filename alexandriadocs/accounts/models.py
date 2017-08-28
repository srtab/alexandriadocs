# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    """ """
    slug = AutoSlugField(populate_from='username', unique=True,
                         always_update=True, db_index=True)
    name = models.CharField(_('name'), max_length=128, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("accounts:index", args=[self.slug])