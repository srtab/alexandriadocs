from accounts.models import AccessLevel


def access_levels(request):
    return AccessLevel.choices_dist
