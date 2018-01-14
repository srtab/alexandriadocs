import os
import shutil
from zipfile import ZipFile
from pathlib import Path

from django.conf import settings as djsettings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from accounts.managers import CollaboratorManager
from accounts.models import AccessLevel, CollaboratorMixin
from autoslug import AutoSlugField
from core.conf import settings
from core.models import VisibilityMixin
from django_extensions.db.models import TimeStampedModel
from groups.models import Group
from projects.managers import ImportedFileManager, ProjectManager
from projects.tokens import token_generator
from projects.utils import projects_upload_to
from projects.validators import StructureValidator, MimeTypeValidator
from taggit.managers import TaggableManager


class Project(VisibilityMixin, TimeStampedModel):
    """
    An project represents a namespace
    """
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, verbose_name=_('group'),
        related_name='projects')
    author = models.ForeignKey(
        djsettings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        verbose_name=_('author'), help_text=_('project author'),
        related_name='projects')
    collaborators = models.ManyToManyField(
        djsettings.AUTH_USER_MODEL, through='ProjectCollaborator',
        related_name='collaborate_projects')
    name = models.CharField(
        _('project name'), max_length=128,
        help_text=_('project name must be unique under the selected group'))
    slug = AutoSlugField(
        _('slug'), populate_from='name', always_update=True,
        unique_with='group_id')
    description = models.CharField(
        _('description'), max_length=256, blank=True, null=True)
    repo = models.URLField(_('repository URL'), max_length=255)
    tags = TaggableManager(blank=True)

    objects = ProjectManager()

    class Meta:
        ordering = ['created']
        verbose_name = _('project')

    def __str__(self):
        return self.name

    @cached_property
    def fullname(self):
        return "{group} / {name}".format(group=self.group, name=self)

    @property
    def is_private(self):
        return bool(self.group.is_private or
                    self.visibility_level == self.Level.PRIVATE)

    @property
    def is_public(self):
        return bool(self.group.is_public or
                    self.visibility_level == self.Level.PUBLIC)

    @cached_property
    def serve_root_path(self):
        return os.path.join(settings.SENDFILE_ROOT, self.slug)

    @cached_property
    def last_imported_archive_date(self):
        try:
            return self.imported_archives.latest('created').created
        except ImportedArchive.DoesNotExist:
            return None

    @cached_property
    def imported_archive_exists(self):
        return self.imported_archives.exists()

    @cached_property
    def imported_files_count(self):
        return self.imported_files.count()

    @cached_property
    def api_token(self):
        return token_generator.make_token(self)

    def get_absolute_url(self):
        return reverse('projects:project-detail', args=[self.slug])

    def get_docs_url(self, filename="index.html"):
        return reverse('serve-docs', args=[self.slug, filename])

    def clean(self):
        # Don't allow repeated titles in same group.
        projects = Project.objects\
            .filter(group_id=self.group_id, name__iexact=self.name)\
            .exclude(id=self.pk)
        if projects.exists():
            raise ValidationError({
                'name': _("Project with this name already exists.")
            })

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        """
        Create default collaborator for the project author with max access
        level.
        """
        if created:
            ProjectCollaborator.objects.create(
                project_id=instance.pk,
                user_id=instance.author_id,
                access_level=AccessLevel.OWNER
            )


post_save.connect(Project.post_save, sender=Project)


class ProjectCollaborator(CollaboratorMixin, TimeStampedModel):
    """ """
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name='project_collaborators')
    objects = CollaboratorManager()

    class Meta:
        unique_together = ('user', 'project')
        index_together = ('user', 'project')
        verbose_name = _('project collaborator')


class ImportedArchive(TimeStampedModel):
    """
    An imported archive holds the result of an static generated site version
    for a project.
    """
    class Source:
        FORM = 0
        API = 1

        choices = (
            (FORM, _('Form')),
            (API, _('API')),
        )

    uploaded_by = models.ForeignKey(
        djsettings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        null=True, verbose_name=_('who uploaded'),
        help_text=_('who uploaded the documentation'))
    uploaded_from = models.PositiveSmallIntegerField(
        _('source'), choices=Source.choices, default=Source.FORM)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name=_('project'),
        related_name='imported_archives')
    archive = models.FileField(
        _('archive'), upload_to=projects_upload_to,
        help_text=_('archive with project documentation.'),
        validators=[
            MimeTypeValidator(
                allowed_mimetypes=settings.ALEXANDRIA_ALLOWED_MIMETYPES),
            StructureValidator()
        ])

    class Meta:
        ordering = ('-created',)
        verbose_name = _('imported archive')

    def __str__(self):
        return self.project.__str__()

    def filesify(self):
        """
        Extract tarfile and launch walk through valid imported files to
        create entries on database with file info to be indexed.
        """
        # clean directory
        shutil.rmtree(self.project.serve_root_path, ignore_errors=True)
        # extract all files
        with ZipFile(self.archive.path) as myzip:
            myzip.extractall(self.project.serve_root_path)
        # register file on database
        ImportedFile.objects.walk(self.project_id,
                                  self.project.serve_root_path)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        """
        Fileyfi the imported archive on each ImportedArchive object creation
        """
        if created:
            instance.filesify()


post_save.connect(ImportedArchive.post_save, sender=ImportedArchive)


class ImportedFile(TimeStampedModel):
    """
    Holds info about html files imported for indexing proposes.
    """
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name=_('project'),
        related_name='imported_files')
    path = models.CharField(_('file path'), max_length=255)
    md5 = models.CharField(_('MD5 checksum'), max_length=255)
    objects = ImportedFileManager()

    class Meta:
        verbose_name = _('imported file')

    def __str__(self):
        return self.path

    def get_absolute_url(self):
        relpath = os.path.relpath(self.path, settings.SENDFILE_ROOT)
        # remove first step of path
        path_parts = Path(relpath).parts
        filepath = os.path.join(*path_parts[1:])
        return self.project.get_docs_url(filepath)
