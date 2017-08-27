# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialAccount
from django import template


register = template.Library()


@register.simple_tag()
def get_providers_unconnected(user):
    unconnected = []
    connected_providers_id = SocialAccount.objects.filter(user=user)\
        .values_list('provider', flat=True)
    for provider in providers.registry.get_list():
        if provider.id not in connected_providers_id:
            unconnected.append(provider)
    return unconnected
