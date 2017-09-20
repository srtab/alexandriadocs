# -*- coding: utf-8 -*-
from django import template
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.inclusion_tag('account/includes/collaborator_list.html',
                        takes_context=True)
def render_inherited_collaborators(context, collaborators):
    instance = context.get('object')
    group_url = reverse(
        'groups:group-collaborators', args=[instance.group.slug])
    anchor = "<a href='{url}'>{group}</a>".format(
        url=group_url, group=instance.group)
    title = _("Collaborators inherited from group {link}")\
        .format(link=anchor)
    return {
        'title': title,
        'collaborator_list': collaborators,
        'show_delete_button': False,
        'show_create_form': False
    }
