from django.contrib import messages


class SuccessDeleteMessageMixin(object):

    def delete(self, request, *args, **kwargs):
        # SuccessMessageMixin not supported on delete views
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.get_success_message())
        return response

    def get_success_message(self):
        return self.success_message % self.object.__dict__


class CacheObjectMixin(object):
    """ """
    def get_object(self):
        if not hasattr(self, 'object'):
            return super().get_object()
        return self.object
