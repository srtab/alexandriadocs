
class AccessCheckerRegistry(object):

    _registry = {}

    def register(self, model_class, checker_class):
        self._registry.update({
            model_class: checker_class()
        })

    def get_checker(self, model_class):
        return self._registry.get(model_class, None)


access_checker_register = AccessCheckerRegistry()
