# -*- coding: utf-8 -*-
from unittest.mock import patch, call

from django.test import SimpleTestCase

from search.signals import AlexandriaSignalProcessor
from projects.models import ImportedFile, Project


class AlexandriaSignalProcessorTest(SimpleTestCase):

    def setUp(self):
        self.processor = AlexandriaSignalProcessor(None, None)

    @patch('search.signals.post_delete')
    @patch('search.signals.post_save')
    def test_setup(self, mpost_save, mpost_delete):
        self.processor.setup()
        mpost_save.connect.assert_has_calls([
            call(self.processor.handle_save, sender=Project),
            call(self.processor.handle_save, sender=ImportedFile),
        ])
        mpost_delete.connect.assert_has_calls([
            call(self.processor.handle_delete, sender=Project),
            call(self.processor.handle_delete, sender=ImportedFile),
        ])

    @patch('search.signals.post_delete')
    @patch('search.signals.post_save')
    def test_teardown(self, mpost_save, mpost_delete):
        self.processor.teardown()
        mpost_save.disconnect.assert_has_calls([
            call(self.processor.handle_save, sender=Project),
            call(self.processor.handle_save, sender=ImportedFile),
        ])
        mpost_delete.disconnect.assert_has_calls([
            call(self.processor.handle_delete, sender=Project),
            call(self.processor.handle_delete, sender=ImportedFile),
        ])
