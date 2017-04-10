from __future__ import unicode_literals

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
from projects.utils import projects_upload_to, extract_files


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
        Organization, verbose_name=_('organization'),
        help_text=_('project organization'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('author'),
        help_text=_('project author'))
    repo = models.CharField(_('repository URL'), max_length=255)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _('project')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "{}{}/".format(settings.PROJECTS_SERVE_URL, self.slug)


@python_2_unicode_compatible
class ProjectArchive(TimeStampedModel):
    """ """
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('who uploaded'),
        help_text=_('who uploaded the documentation'))
    project = models.ForeignKey(Project, verbose_name=_('project'))
    archive = models.FileField(
        _('archive'), upload_to=projects_upload_to,
        help_text=_('archive with project documentation'),
        validators=[
            MimeTypeValidator(
                allowed_mimetypes=settings.PROJECTS_ALLOWED_MIMETYPES)
        ])

    class Meta:
        verbose_name = _('project archive')

    def __str__(self):
        return self.project.__str__()

    @staticmethod
    def post_save(sender, instance, **kwargs):
        """Extract the archive and put files to be served"""
        extract_files(instance.project.slug, instance.archive)


post_save.connect(ProjectArchive.post_save, sender=ProjectArchive)
