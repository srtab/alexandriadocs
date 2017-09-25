from django.apps import apps
from django.conf import settings
from django.utils.crypto import salted_hmac
from django.utils.http import base36_to_int, int_to_base36


class ApiTokenGenerator(object):
    """
    Strategy object used to generate and check tokens.
    """
    key_salt = "projects.tokens.ApiTokenGenerator"
    secret = settings.SECRET_KEY

    def make_token(self, project):
        """
        Return a token that can be used to upload archives throug the API.
        After hash is calculated, we concat the project id in order to simplify
        the token check, otherwise we would have to go through all the objects
        in the database.
        """
        project_b36 = int_to_base36(project.pk)
        digest = salted_hmac(
            self.key_salt,
            self._make_hash_value(project),
            secret=self.secret,
        ).hexdigest()
        return "{project}-{digest}".format(
            project=project_b36, digest=digest)

    def _make_hash_value(self, project):
        return str(project.pk) + str(project.author_id) + str(project.group_id)

    def check_token(self, token):
        """
        Check that a token is correct and corresponds to an existent project.
        """
        if not token:
            return False
        project = self.get_project(token)
        return bool(project and self.make_token(project) == token)

    def get_project(self, token):
        # to avoid circular imports
        Project = apps.get_model('projects', 'Project')  # NOQA
        project_id = self.get_project_id(token)
        if not project_id:
            return None
        return Project.objects.filter(pk=project_id).first()

    def get_project_id(self, token):
        try:
            project_b36, digest = token.split("-")
            project_id = base36_to_int(project_b36)
        except ValueError:
            return None
        return project_id


token_generator = ApiTokenGenerator()
