# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from crispy_forms.helper import FormHelper
from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.html import escape
from django.utils.http import urlencode


register = template.Library()
context_processor_error_msg = (
    'Tag {%% %s %%} requires django.template.context_processors.request to be '
    'in the template configuration'
)


@register.assignment_tag(takes_context=True)
def is_current_url(context, namespace=None, url_name=None):
    if 'request' not in context:
        raise ImproperlyConfigured(context_processor_error_msg % 'menu_active')
    request = context.get('request')
    check = True
    if namespace:
        check = check and namespace == request.resolver_match.namespace
    if url_name:
        check = check and url_name == request.resolver_match.url_name
    return check


@register.simple_tag(takes_context=True)
def menu_active(context, namespace=None, url_name=None, css_class='active'):
    return css_class if is_current_url(context, namespace, url_name) else ''


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


@register.inclusion_tag("includes/sentry_ravenjs.html")
def sentry_ravenjs():
    return {
        'SENTRY': getattr(settings, 'SENTRY_CONFIG', None)
    }


@register.assignment_tag()
def form_helper(**kwargs):
    helper = FormHelper()
    for attr, value in kwargs.items():
        if hasattr(helper, attr):
            setattr(helper, attr, value)
    return helper
