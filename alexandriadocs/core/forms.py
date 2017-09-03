# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper


class UntaggedFormMixin(object):
    """Mixin to avoid crispy showing fields labels and rendering de form tag"""
    def __init__(self, *args, **kwargs):
        super(UntaggedFormMixin, self).__init__(*args, **kwargs)
        if not hasattr(self, 'helper'):
            self.helper = FormHelper()
        self.helper.form_tag = False


class UnlabeledFormMixin(object):
    """Mixin to avoid crispy showing fields labels and rendering de form tag"""
    def __init__(self, *args, **kwargs):
        super(UnlabeledFormMixin, self).__init__(*args, **kwargs)
        if not hasattr(self, 'helper'):
            self.helper = FormHelper()
        self.helper.form_show_labels = False
