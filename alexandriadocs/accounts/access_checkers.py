

class AccessChecker(object):
    """ """
    model = None

    def get_object(self, user, obj):
        if not hasattr(self, '_object'):
            try:
                self._object = self.model._default_manager.get(
                    user=user, group=obj)
            except self.model.DoesNotExist:
                self._object = None
        return self._object

    def has_access(self, user, obj, access_level):
        return False

    def get_access_level(self, user, obj):
        return 0
