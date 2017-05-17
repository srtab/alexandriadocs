from __future__ import unicode_literals

from rest_framework import serializers

from projects.models import ImportedArchive


class ImportedArchiveSerializer(serializers.ModelSerializer):
    """ """
    class Meta:
        model = ImportedArchive
        fields = ('project', 'archive')
