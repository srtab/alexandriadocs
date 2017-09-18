from accounts.access_checkers import AccessChecker
from accounts.decorators import access_checker
from groups.access_checkers import GroupAccessChecker
from projects.models import Project, ProjectCollaborator


@access_checker(Project)
class ProjectAccessChecker(AccessChecker):
    """ """
    model = ProjectCollaborator
    object_field_name = 'project'

    def __init__(self):
        super().__init__()
        self.group_checker = GroupAccessChecker()

    def has_access(self, user, obj, access_level):
        collaborator = self.get_object(user, obj)
        if not collaborator:
            return self.group_checker.has_access(user, obj.group, access_level)
        return collaborator.access_level >= access_level

    def get_access_level(self, user, obj):
        collaborator = self.get_object()
        if not collaborator:
            return self.group_checker.get_access_level(user, obj)
        return collaborator.access_level
