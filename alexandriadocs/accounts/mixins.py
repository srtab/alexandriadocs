from accounts.models import AccessLevel
from accounts.register import access_checker_register
from core.mixins import CacheObjectMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class HasAccessLevelMixin(CacheObjectMixin, UserPassesTestMixin):
    """ """
    allowed_access_level = AccessLevel.READER
    raise_exception = True

    def test_func(self):
        access_checker = access_checker_register.get_checker(self.model)
        return access_checker.has_access(
            self.request.user, self.get_object(), self.allowed_access_level)
