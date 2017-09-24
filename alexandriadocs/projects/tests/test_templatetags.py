# -*- coding: utf-8 -*-
from core.tests.utils import TemplateTagsTest
from django.test import SimpleTestCase
from groups.models import Group
from projects.models import Project


class RenderInheritedCollaboratorsTest(TemplateTagsTest, SimpleTestCase):

    def setUp(self):
        self.project = Project(group=Group(title='title', slug='slug'))

    def test_render(self):
        template = (
            '{% load projects_tags %}'
            '{% render_inherited_collaborators object_list %}'
        )
        result = self.render_template(template, {
            'object': self.project,
            'object_list': []
        })
        self.assertInHTML(
            'Collaborators inherited from group '
            '<a href="/groups/slug/collaborators/">title</a>', result)
        self.assertInHTML('No associated collaborators.', result)
