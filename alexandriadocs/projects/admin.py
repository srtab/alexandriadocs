from __future__ import unicode_literals

from django.contrib import admin
from projects.models import (
    ImportedArchive, ImportedFile, Organization, Project)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """ """


class ImportedArchiveInline(admin.TabularInline):
    """ """
    model = ImportedArchive


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """ """
    inlines = [
        ImportedArchiveInline,
    ]


@admin.register(ImportedFile)
class ImportedFileAdmin(admin.ModelAdmin):
    """ """
