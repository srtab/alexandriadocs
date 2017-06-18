# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured
from django.utils.http import urlencode
from django.utils.html import escape
from django.conf import settings
from django import template


register = template.Library()
context_processor_error_msg = (
    'Tag {%% %s %%} requires django.template.context_processors.request to be '
    'in the template configuration'
)


@register.simple_tag(takes_context=True)
def menu_active(context, namespace=None, url_name=None, css_class='active'):
    if 'request' not in context:
        raise ImproperlyConfigured(context_processor_error_msg % 'menu_active')
    request = context.get('request')
    check = True
    if namespace:
        check = check and namespace == request.resolver_match.namespace
    if url_name:
        check = check and url_name == request.resolver_match.url_name
    return css_class if check else ''


@register.simple_tag(takes_context=True)
def querystring(context, **kwargs):
    if 'request' not in context:
        raise ImproperlyConfigured(context_processor_error_msg % 'querystring')
    params = dict(context.get('request').GET)
    ordered = OrderedDict()
    ordered.update(params)
    ordered.update(kwargs)
    return escape('?' + urlencode(ordered, doseq=True))


@register.inclusion_tag("includes/analytics-tracking.html")
def analytics_tracking():
    return {
        'TRACKING_ID': getattr(settings, 'ANALYTICS_TRACKING_ID', None)
    }
