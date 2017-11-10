# -*- coding: utf-8 -*-
from api.permissions import HasAPIAccess
from api.serializers import ImportedArchiveSerializer
from projects.models import ImportedArchive
from projects.tokens import token_generator
from rest_framework.generics import CreateAPIView


class ImportedArchiveView(CreateAPIView):
    """ """
    permission_classes = (HasAPIAccess,)
    serializer_class = ImportedArchiveSerializer

    def perform_create(self, serializer):
        api_token = self.request.META.get('HTTP_API_KEY', None)
        project_id = token_generator.get_project_id(api_token)
        serializer.save(
            uploaded_from=ImportedArchive.Source.API,
            project_id=project_id
        )
