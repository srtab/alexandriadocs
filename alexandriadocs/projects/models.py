from __future__ import unicode_literals

import tarfile
import os

from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import models

from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import (
    TitleSlugDescriptionModel, TimeStampedModel)
from taggit.managers import TaggableManager

from projects.validators import MimeTypeValidator, IntegrityTarValidator
from projects.managers import ImportedFileManager
from projects.utils import projects_upload_to


@python_2_unicode_compatible
class Organization(TimeStampedModel):
    """An organization represents a group of projects.
    """
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='name')

    class Meta:
        verbose_name = _('organization')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Project(TitleSlugDescriptionModel, TimeStampedModel):
    """An project represents a namespace.
    """
    organization = models.ForeignKey(
        Organization, models.PROTECT, verbose_name=_('organization'),
        help_text=_('project organization'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT, verbose_name=_('author'),
        help_text=_('project author'))
    repo = models.CharField(_('repository URL'), max_length=255)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _('project')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "{}{}/index.html".format(settings.PROJECTS_SERVE_URL, self.slug)

    @property
    def serve_root_path(self):
        return os.path.join(settings.PROJECTS_SERVE_ROOT, self.slug)


@python_2_unicode_compatible
class ImportedArchive(TimeStampedModel):
    """An imported archive holds the result of an static generated site version
    for a project.
    """
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT,
        verbose_name=_('who uploaded'),
        help_text=_('who uploaded the documentation'))
    project = models.ForeignKey(
        Project, models.CASCADE, verbose_name=_('project'))
    archive = models.FileField(
        _('archive'), upload_to=projects_upload_to,
        help_text=_('archive with project documentation.'),
        validators=[
            MimeTypeValidator(
                allowed_mimetypes=settings.PROJECTS_ALLOWED_MIMETYPES),
            IntegrityTarValidator(settings.PROJECTS_SERVE_ROOT)
        ])

    class Meta:
        verbose_name = _('imported archive')

    def __str__(self):
        return self.project.__str__()

    def fileify(self):
        """Extract tarfile and launch walk through valid imported files to
        create entries on database with file info to be indexed.
        """
        with tarfile.open(self.archive.path, "r:gz") as tar:
            tar.extractall(self.project.serve_root_path)
        ImportedFile.objects.walk(self.project_id,
                                  self.project.serve_root_path)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        """Fileyfi the imported archive on each ImportedArchive object creation
        """
        if created:
            instance.fileify()


post_save.connect(ImportedArchive.post_save, sender=ImportedArchive)


@python_2_unicode_compatible
class ImportedFile(TimeStampedModel):
    """Holds info about html files imported for indexing proposes.
    """
    project = models.ForeignKey(
        Project, models.CASCADE, verbose_name=_('project'))
    path = models.CharField(_('file path'), max_length=255)
    md5 = models.CharField(_('MD5 checksum'), max_length=255)
    objects = ImportedFileManager()

    class Meta:
        verbose_name = _('imported file')

    def __str__(self):
        return self.path

    def get_absolute_url(self):
        relpath = os.path.relpath(self.path, settings.PROJECTS_SERVE_ROOT)
        return settings.PROJECTS_SERVE_URL + relpath
