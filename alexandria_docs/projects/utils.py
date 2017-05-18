from __future__ import unicode_literals

from django.utils import timezone


def projects_upload_to(instance, filename):
    """construct path to uploaded project archives"""
    today = timezone.now().strftime("%Y/%m")
    return "projects/{date}/{slug}/{filename}".format(
        date=today, slug=instance.project.slug, filename=filename)
