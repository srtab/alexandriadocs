# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class SubdomainMiddleware(object):
    """ """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """ """
        host = request.get_host().lower()
        domain_parts = host.split('.')

        if len(domain_parts) == 2:
            subdomain = domain_parts[0]
            request.slug = subdomain
            request.urlconf = 'alexandriadocs.urls.subdomains'

        response = self.get_response(request)

        return response
