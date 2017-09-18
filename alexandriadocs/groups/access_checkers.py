from accounts.access_checkers import AccessChecker
from accounts.decorators import access_checker
from groups.models import Group, GroupCollaborator


@access_checker(Group)
class GroupAccessChecker(AccessChecker):
    """ """
    model = GroupCollaborator

    def has_access(self, user, obj, access_level):
        collaborator = self.get_object(user, obj)
        return bool(collaborator and collaborator.access_level >= access_level)

    def get_access_level(self, user, obj):
        collaborator = self.get_object()
        if not collaborator:
            return None
        return collaborator.access_level
