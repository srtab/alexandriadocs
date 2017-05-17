from __future__ import unicode_literals

from django.contrib import admin

from projects.models import Organization, Project, ImportedArchive


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
