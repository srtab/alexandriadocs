from django.conf import settings
from django.utils.crypto import salted_hmac


class ApiTokenGenerator(object):
    """
    Strategy object used to generate and check tokens.
    """
    key_salt = "projects.tokens.ApiTokenGenerator"
    secret = settings.SECRET_KEY

    def make_token(self, project):
        """
        Return a token that can be used to upload archives throug the API.
        """
        return salted_hmac(
            self.key_salt,
            self._make_hash_value(project),
            secret=self.secret,
        ).hexdigest()

    def check_token(self, project, token):
        """
        Check that a token is correct for a given project.
        """
        if not (project and token):
            return False
        return self.make_token(project) == token

    def _make_hash_value(self, project):
        return str(project.pk) + str(project.group_id)


token_generator = ApiTokenGenerator()
