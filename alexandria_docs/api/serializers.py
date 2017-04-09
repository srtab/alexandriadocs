from __future__ import unicode_literals

from rest_framework import serializers

from projects.models import ProjectArchive


class ProjectArchiveSerializer(serializers.ModelSerializer):
    """ """
    class Meta:
        model = ProjectArchive
        fields = ('project', 'archive')
