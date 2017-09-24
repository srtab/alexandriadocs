# -*- coding: utf-8 -*-
from accounts.managers import CollaboratorManager
from accounts.models import AccessLevel, CollaboratorMixin
from core.models import TitleSlugDescriptionMixin, VisibilityMixin
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from groups.managers import GroupManager


class Group(VisibilityMixin, TitleSlugDescriptionMixin, TimeStampedModel):
    """
    House several projects under the same namespace, just like a folder
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='GroupCollaborator',
        related_name='collaborate_groups')
    objects = GroupManager()

    class Meta:
        ordering = ['title', 'created']
        verbose_name = _('group')

    def __str__(self):
        return self.title

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
