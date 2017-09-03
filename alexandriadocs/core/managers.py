# -*- coding: utf-8 -*-
from django.db import models


class VisibilityQuerySet(models.QuerySet):

    def public(self):
        return self.filter(visibility_level=self.model.Level.PUBLIC)

    def private(self):
        return self.filter(visibility_level=self.model.Level.PRIVATE)
