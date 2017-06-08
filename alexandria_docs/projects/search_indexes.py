# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import logging

from haystack import indexes
from pyquery import PyQuery

from projects.models import Project, ImportedFile


logger = logging.getLogger('alexandria.search')


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    """Index main project info"""
    text = indexes.CharField(
        document=True, use_template=True,
        template_name="projects/search/project.txt")
    title = indexes.CharField(model_attr='title')
    absolute_url = indexes.CharField()

    def get_model(self):
        return Project

    def prepare_absolute_url(self, obj):
        return obj.get_absolute_url()


class ImportedFileIndex(indexes.SearchIndex, indexes.Indexable):
    """Index imported files"""
    text = indexes.CharField(
        document=True, template_name="projects/search/imported_file.txt")
    created = indexes.DateTimeField(model_attr='created')
    title = indexes.CharField()
    absolute_url = indexes.CharField()

    def get_model(self):
        return ImportedFile

    def prepare_absolute_url(self, obj):
        return obj.get_absolute_url()

    def prepare(self, obj):
        """Open the expected .html file and extract body and title to index"""
        data = super(ImportedFileIndex, self).prepare(obj)
        rich_content = ImportedFileIndex.extract_rich_content(obj)
        if rich_content:
            # inject the object to the template with the rich content extracted
            rich_content['object'] = obj
            data['title'] = rich_content['title']
            data['text'] = self.fields['text'].prepare_template(rich_content)
        return data

    @staticmethod
    def extract_rich_content(obj):
        rich_content = {}
        try:
            with codecs.open(obj.path, encoding='utf-8', mode='r') as f:
                content = f.read()
            doc = PyQuery(content)
            title = ImportedFileIndex.extract_title(doc)
            rich_content['title'] = title
            rich_content['body'] = doc('body').html()
        except IOError as e:
            logger.error(
                'Search Index: Unable to index file project=%s path=%s',
                obj.project, obj.path, exc_info=e)
            return None
        except ValueError as e:
            # Pyquery raises ValueError if body or title doesn't exist
            logger.warning(
                'Search Index: no body/title found project=%s path=%s',
                obj.project, obj.path, exc_info=e)
            return None
        logger.info('Search Index: indexing file project=%s path=%s length=%s',
                    obj.project, obj.path, len(rich_content['body']))
        return rich_content

    @staticmethod
    def extract_title(doc):
        title = None
        try:
            title = doc('body h1').text().strip()
        except ValueError:
            pass
        if not title:
            try:
                title = doc('head title').text().strip()
            except ValueError:
                raise
        return title.replace('¶', '')
