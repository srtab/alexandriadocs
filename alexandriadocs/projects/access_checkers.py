from accounts.access_checkers import AccessChecker
from accounts.decorators import access_checker
from groups.access_checkers import group_access_checker
from projects.models import Project, ProjectCollaborator


@access_checker(Project)
class ProjectAccessChecker(AccessChecker):
    """ """
    model = ProjectCollaborator
    object_field_name = 'project'

    def __init__(self):
        super().__init__()

    def has_access(self, user, obj, access_level):
        collaborator = self.get_object(user, obj)
        has_access = group_access_checker.has_access(
            user, obj.group, access_level)
        if not collaborator:
            return has_access
        return has_access or collaborator.access_level >= access_level

    def get_access_level(self, user, obj):
        collaborator = self.get_object()
        if not collaborator:
            return group_access_checker.get_access_level(user, obj)
        return collaborator.access_level


project_access_checker = ProjectAccessChecker()
