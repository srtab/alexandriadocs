from __future__ import unicode_literals

import codecs
import logging

from haystack import indexes
from pyquery import PyQuery

from projects.models import Project, ImportedFile
from projects.utils import clean_html


logger = logging.getLogger('alexandria.search')


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    """Index main project info"""
    text = indexes.CharField(document=True, model_attr='description')
    title = indexes.CharField(model_attr='title')
    author = indexes.CharField(model_attr='author__username')
    absolute_url = indexes.CharField()

    def get_model(self):
        return Project

    def prepare_absolute_url(self, obj):
        return obj.get_absolute_url()


class ImportedFileIndex(indexes.SearchIndex, indexes.Indexable):
    """Index imported files"""
    text = indexes.CharField(document=True)
    project = indexes.CharField(model_attr='project__title')
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
        try:
            with codecs.open(obj.path, encoding='utf-8', mode='r') as f:
                content = f.read()
        except IOError as e:
            logger.error(
                'Search Index: Unable to index file project=%s path=%s',
                obj.project, obj.path, exc_info=e)
            return data
        try:
            doc = PyQuery(content)
            title = doc('head title').html()
            body = doc('body').html()
        except ValueError:
            # Pyquery raises ValueError if body doesn't exist
            logger.warning(
                'Search Index: no body/title found project=%s path=%s',
                obj.project, obj.path, exc_info=e)
            return data
        title_to_index = clean_html(title) or obj.name
        body_to_index = clean_html(body)
        if not body_to_index:
            logger.warning(
                'Search Index: body without content project=%s path=%s',
                obj.project, obj.path)
            return data
        logger.info('Search Index: indexing file project=%s path=%s length=%s',
                    obj.project, obj.path, len(body_to_index))
        data['title'] = title_to_index
        data['text'] = body_to_index
        return data
