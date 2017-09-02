from api.serializers import ImportedArchiveSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


class ImportArchiveView(CreateAPIView):
    """ """
    permission_classes = (IsAuthenticated,)
    serializer_class = ImportedArchiveSerializer

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
