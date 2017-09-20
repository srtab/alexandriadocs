# -*- coding: utf-8 -*-
from accounts.register import access_checker_register
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


@register.assignment_tag(takes_context=True)
def has_access(context, access_level, obj):
    request = context.get('request')
    if request.user.is_authenticated:
        access_checker = access_checker_register.get_checker(obj._meta.model)
        return access_checker.has_access(request.user, obj, access_level)
    return False


@register.inclusion_tag('account/includes/collaborator_list.html',
                        takes_context=True)
def render_collaborator_list(context, collaborators, create_url_name,
                             delete_url_name, title=None):
    return {
        'form': context.get('form'),
        'object': context.get('object'),
        'title': title,
        'collaborator_list': collaborators,
        'create_url_name': create_url_name,
        'delete_url_name': delete_url_name,
        'show_delete_button': True,
        'show_create_form': True
    }
