from __future__ import unicode_literals

import tarfile
import hashlib
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

from projects.validators import MimeTypeValidator
from projects.utils import projects_upload_to


@python_2_unicode_compatible
class Organization(TimeStampedModel):
    """ """
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='name')

    class Meta:
        verbose_name = _('organization')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Project(TitleSlugDescriptionModel, TimeStampedModel):
    """ """
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


@python_2_unicode_compatible
class ImportedArchive(TimeStampedModel):
    """ """
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT,
        verbose_name=_('who uploaded'),
        help_text=_('who uploaded the documentation'))
    project = models.ForeignKey(
        Project, models.CASCADE, verbose_name=_('project'))
    archive = models.FileField(
        _('archive'), upload_to=projects_upload_to,
        help_text=_('archive with project documentation'),
        validators=[
            MimeTypeValidator(
                allowed_mimetypes=settings.PROJECTS_ALLOWED_MIMETYPES)
        ])

    class Meta:
        verbose_name = _('imported archive')

    def __str__(self):
        return self.project.__str__()

    @property
    def extract_path(self):
        return os.path.join(settings.PROJECTS_SERVE_ROOT, self.project.slug)

    @staticmethod
    def post_save(sender, instance, **kwargs):
        """Extract the archive and put files to be served"""
        with tarfile.open(instance.archive.path, "r:gz") as tar:
            tar.extractall(instance.extract_path)

        for root, __, filenames in os.walk(instance.extract_path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                md5 = hashlib.md5(open(full_path, 'rb').read()).hexdigest()
                obj, __ = ImportedFile.objects.update_or_create(
                    imported_archive=instance,
                    name=filename,
                    path=full_path,
                    defaults={
                        'md5': md5
                    }
                )


post_save.connect(ImportedArchive.post_save, sender=ImportedArchive)


@python_2_unicode_compatible
class ImportedFile(TimeStampedModel):
    """ """
    imported_archive = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_('archive'))
    name = models.CharField(_('Name'), max_length=255)
    path = models.FilePathField(
        path=settings.PROJECTS_SERVE_ROOT, match=".*\.html$", recursive=True,
        max_length=255)
    md5 = models.CharField(_('MD5 checksum'), max_length=255)

    class Meta:
        verbose_name = _('imported file')

    def __str__(self):
        return self.name
