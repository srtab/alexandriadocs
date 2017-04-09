from __future__ import unicode_literals

from django.contrib import admin

from projects.models import Organization, Project, ProjectArchive


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """ """


class ProjectArchiveInline(admin.TabularInline):
    """ """
    model = ProjectArchive


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """ """
    inlines = [
        ProjectArchiveInline,
    ]
