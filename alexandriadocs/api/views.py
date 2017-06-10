from __future__ import unicode_literals

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView

from api.serializers import ImportedArchiveSerializer


class ImportArchiveView(CreateAPIView):
    """ """
    permission_classes = (IsAuthenticated,)
    serializer_class = ImportedArchiveSerializer

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
