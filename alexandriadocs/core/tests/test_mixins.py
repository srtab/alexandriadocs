# -*- coding: utf-8 -*-
from core.mixins import CacheObjectMixin, SuccessDeleteMessageMixin
from django.test import SimpleTestCase
from django.views.generic.edit import DeleteView, UpdateView
from mock import Mock, patch


class SuccessDeleteMessageMixinTest(SimpleTestCase):

    class TestDeleteView(SuccessDeleteMessageMixin, DeleteView):
        success_message = 'Success'
        object = Mock()

    @patch.object(DeleteView, 'delete')
    @patch('core.mixins.messages')
    def test_delete(self, mmessages, mdelete):
        view = self.TestDeleteView()
        view.delete('request')
        mdelete.assert_called_with('request')
        mmessages.success.assert_called_with('request', 'Success')

    def test_get_success_message(self):
        view = self.TestDeleteView()
        self.assertEqual(view.get_success_message(), 'Success')


class CacheObjectMixinTest(SimpleTestCase):

    class TestCacheView(CacheObjectMixin, UpdateView):
        pass

    @patch.object(UpdateView, 'get_object', return_value='object')
    def test_get_object(self, mget_object):
        view = self.TestCacheView()
        view.get_object()
        self.assertTrue(hasattr(view, 'object'))
        self.assertEqual(view.get_object(), 'object')
