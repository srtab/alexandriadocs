# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from groups.models import Group
from projects.models import Project


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return [
            'homepage', 'account_login', 'account_signup',
            'account_reset_password', 'search:index', 'search:pages'
        ]

    def location(self, item):
        return reverse(item)


class ProjectViewSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return Project.objects.public()

    def lastmod(self, obj):
        return obj.modified


class GroupViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return Group.objects.public()

    def lastmod(self, obj):
        return obj.modified


sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectViewSitemap,
    'groups': GroupViewSitemap
}
