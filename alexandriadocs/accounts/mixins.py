from django.contrib.auth.mixins import UserPassesTestMixin

from accounts.models import AccessLevel
from accounts.register import access_checker_register
from core.mixins import CacheObjectMixin


class HasAccessLevelMixin(CacheObjectMixin, UserPassesTestMixin):
    """ """
    allowed_access_level = AccessLevel.READER
    raise_exception = True

    def access_object(self):
        return self.get_object()

    def test_func(self):
        obj = self.access_object()
        access_checker = access_checker_register.get_checker(obj._meta.model)
        return access_checker.has_access(
            self.request.user, obj, self.allowed_access_level)
