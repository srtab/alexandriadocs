# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper


class FormHelperMixin(object):
    """ """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class UntaggedFormMixin(FormHelperMixin):
    """Mixin to avoid crispy showing fields labels and rendering de form tag"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False


class UnlabeledFormMixin(FormHelperMixin):
    """Mixin to avoid crispy showing fields labels and rendering de form tag"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_show_labels = False
