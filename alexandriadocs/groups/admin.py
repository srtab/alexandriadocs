from django.contrib import admin

from groups.models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """ """
