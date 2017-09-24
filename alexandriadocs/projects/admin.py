from django.contrib import admin
from projects.models import ImportedArchive, ImportedFile, Project


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
