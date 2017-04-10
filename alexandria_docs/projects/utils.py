from __future__ import unicode_literals

import os
import tarfile

from django.utils import timezone
from django.conf import settings


def projects_upload_to(instance, filename):
    """construct path to uploaded project archives"""
    today = timezone.now().strftime("%Y/%m")
    return "projects/{date}/{slug}/{filename}".format(
        date=today, slug=instance.project.slug, filename=filename)


def extract_to(name):
    """ """
    return os.path.join(settings.PROJECTS_SERVE_ROOT, name)


def extract_files(name, archive):
    """ """
    with tarfile.open(archive.path, "r:gz") as tar:
        tar.extractall(extract_to(name))
