from django.forms.widgets import Select


class Select2Mixin(object):
    """ """

    def __init__(self, url=None, *args, **kwargs):
        """Instanciate a widget with a URL and a list of fields to forward."""
        self.url = url
        super().__init__(*args, **kwargs)

    def build_attrs(self, *args, **kwargs):
        """ """
        attrs = super().build_attrs(*args, **kwargs)
        if self.url is not None:
            attrs['data-autocomplete-url'] = self.url
        return attrs


class Select2(Select2Mixin, Select):
    """ """
