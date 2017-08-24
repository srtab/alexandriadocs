# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.utils.html import strip_tags


def projects_upload_to(instance, filename):
    """construct path to uploaded project archives"""
    today = timezone.now().strftime("%Y/%m")
    return "projects/{date}/{slug}/{filename}".format(
        date=today, slug=instance.project.slug, filename=filename)


def clean_html(value):
    return strip_tags(value).replace('¶', '')
