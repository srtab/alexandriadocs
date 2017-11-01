from django.db.models.signals import post_delete, post_save

from haystack.signals import BaseSignalProcessor
from projects.models import ImportedFile, Project


class AlexandriaSignalProcessor(BaseSignalProcessor):

    register_models = [Project, ImportedFile]

    def setup(self):
        for model in self.register_models:
            post_save.connect(self.handle_save, sender=model)
            post_delete.connect(self.handle_delete, sender=model)

    def teardown(self):
        for model in self.register_models:
            post_save.disconnect(self.handle_save, sender=model)
            post_delete.disconnect(self.handle_delete, sender=model)
