import os
import tarfile

from core.models import TitleSlugDescriptionMixin, VisibilityMixin
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from groups.models import Group
from projects.managers import ImportedFileManager, ProjectManager
from projects.tokens import token_generator
from projects.utils import projects_upload_to
from projects.validators import MimeTypeValidator
from taggit.managers import TaggableManager


class Project(VisibilityMixin, TitleSlugDescriptionMixin, TimeStampedModel):
    """An project represents a namespace
    """
    group = models.ForeignKey(
        Group, models.PROTECT, verbose_name=_('group'),
        help_text=_('Just like a folder, helps you to organize you projects'),
        related_name='projects')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT, verbose_name=_('author'),
        help_text=_('project author'), related_name='projects')
    repo = models.CharField(_('repository URL'), max_length=255)
    tags = TaggableManager(blank=True)

    objects = ProjectManager()

    class Meta:
        verbose_name = _('project')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "{}{}/index.html".format(settings.PROJECTS_SERVE_URL, self.slug)

    @property
    def serve_root_path(self):
        return os.path.join(settings.PROJECTS_SERVE_ROOT, self.slug)

    @cached_property
    def last_imported_archive_date(self):
        try:
            return self.imported_archives.latest('created').created
        except ImportedArchive.DoesNotExist:
            return None

    @cached_property
    def api_token(self):
        return token_generator.make_token(self)


class ImportedArchive(TimeStampedModel):
    """An imported archive holds the result of an static generated site version
    for a project.
    """
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT,
        verbose_name=_('who uploaded'),
        help_text=_('who uploaded the documentation'))
    project = models.ForeignKey(
        Project, models.CASCADE, verbose_name=_('project'),
        related_name='imported_archives')
    archive = models.FileField(
        _('archive'), upload_to=projects_upload_to,
        help_text=_('archive with project documentation.'),
        validators=[
            MimeTypeValidator(
                allowed_mimetypes=settings.PROJECTS_ALLOWED_MIMETYPES)
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
