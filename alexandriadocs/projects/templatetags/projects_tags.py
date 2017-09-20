# -*- coding: utf-8 -*-
from django import template
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from groups.models import GroupCollaborator


register = template.Library()


@register.inclusion_tag('account/includes/collaborator_list.html',
                        takes_context=True)
def render_inherited_collaborators(context, collaborators):
    instance = context.get('object')
    group_collaborators = GroupCollaborator.objects\
        .filter(group_id=instance.group_id)\
        .exclude(user_id__in=collaborators.values('user_id'))
    if group_collaborators.exists():
        group_url = reverse(
            'groups:group-collaborators', args=[instance.group.slug])
        anchor = "<a href='{url}'>{group}</a>".format(
            url=group_url, group=instance.group)
        title = _("Collaborators inherited from group {link}")\
            .format(link=anchor)
        return {
            'title': title,
            'collaborator_list': group_collaborators,
            'show_delete_button': False,
            'show_create_form': False
        }
    return {
        'hide_list': True
    }
