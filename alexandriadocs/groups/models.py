# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from accounts.managers import CollaboratorManager
from accounts.models import AccessLevel, CollaboratorMixin
from autoslug import AutoSlugField
from core.models import VisibilityMixin
from django_extensions.db.models import TimeStampedModel
from groups.managers import GroupManager


class Group(VisibilityMixin, TimeStampedModel):
    """
    House several projects under the same namespace, just like a folder
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='GroupCollaborator',
        related_name='collaborate_groups')
    name = models.CharField(_('group name'), max_length=64, unique=True)
    slug = AutoSlugField(_('slug'), populate_from='name', always_update=True)
    description = models.CharField(
        _('description'), max_length=256, blank=True, null=True)
    objects = GroupManager()

    class Meta:
        ordering = ['name', 'created']
        verbose_name = _('group')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('groups:group-detail', args=[self.slug])

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        """
        Create default collaborator for the group author with max access level.
        """
        if created:
            GroupCollaborator.objects.create(
                group_id=instance.pk,
                user_id=instance.author_id,
                access_level=AccessLevel.OWNER
            )


post_save.connect(Group.post_save, sender=Group)


class GroupCollaborator(CollaboratorMixin, TimeStampedModel):
    """ """
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='group_collaborators')
    objects = CollaboratorManager()

    class Meta:
        unique_together = ('user', 'group')
        index_together = ('user', 'group')
        verbose_name = _('group collaborator')
