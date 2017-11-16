# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter
def extract_objects(result_list, method=None):
    if method == 'only_objects':
        return [result.object for result in result_list]
    return [(result, result.object) for result in result_list]
