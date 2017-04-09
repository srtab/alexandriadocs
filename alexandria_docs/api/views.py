from __future__ import unicode_literals

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView

from api.serializers import ProjectArchiveSerializer


class UploadProjectArchiveView(CreateAPIView):
    """ """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectArchiveSerializer

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
