# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def menu_active(context, namespace=None, url_name=None, css_class='active'):
    request = context.get('request')
    check = True
    if namespace:
        check = check and namespace == request.resolver_match.namespace
    if url_name:
        check = check and url_name == request.resolver_match.url_name
    return css_class if check else ''
