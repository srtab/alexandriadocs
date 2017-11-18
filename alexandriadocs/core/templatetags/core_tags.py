# -*- coding: utf-8 -*-
from collections import OrderedDict

from django import template
from django.conf import settings
from django.utils.html import escape
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

register = template.Library()


GITHUB_HOSTNAME = 'github'
GITLAB_HOSTNAME = 'gitlab'
BITBUCKET_HOSTNAME = 'bitbucket'


@register.assignment_tag(takes_context=True)
def is_current_url(context, namespace=None, url_name=None):
    request = context.get('request')
    if request.resolver_match:
        check = True
        if namespace:
            check = check and namespace == request.resolver_match.namespace
        if url_name:
            check = check and url_name == request.resolver_match.url_name
        return check
    return False


@register.simple_tag(takes_context=True)
def menu_active(context, namespace=None, url_name=None, css_class='active'):
    return css_class if is_current_url(context, namespace, url_name) else ''


@register.simple_tag(takes_context=True)
def querystring(context, **kwargs):
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


@register.inclusion_tag("includes/sentry-ravenjs.html")
def sentry_ravenjs():
    return {
        'SENTRY': getattr(settings, 'SENTRY_CONFIG', None)
    }


@register.simple_tag(takes_context=True)
def body_class(context):
    request = context.get('request')
    if request.resolver_match:
        namespace = request.resolver_match.namespace
        url_name = request.resolver_match.url_name
        if namespace:
            return "view-{namespace}-{url_name}".format(
                namespace=namespace, url_name=url_name)
        return "view-{url_name}".format(url_name=url_name)
    return "view-noresolver-match"


@register.inclusion_tag("core/includes/visibility_icon.html")
def visibility_icon(visibility_obj):
    return {
        'visibility_obj': visibility_obj,
    }


@register.simple_tag(takes_context=True)
def absolute_uri(context, location):
    request = context.get('request')
    return request.build_absolute_uri(location)


@register.filter()
def repo_icon(value):
    icon = 'fa-git-square', 'Source'
    if GITHUB_HOSTNAME in value:
        icon = 'fa-github', 'Github'
    elif GITLAB_HOSTNAME in value:
        icon = 'fa-gitlab', 'Gitlab'
    elif BITBUCKET_HOSTNAME in value:
        icon = 'fa-bitbucket', 'Bitbucket'
    return mark_safe(
        '<i class="fa fa-fw {}" aria-hidden="true"></i> {}'.format(*icon))
